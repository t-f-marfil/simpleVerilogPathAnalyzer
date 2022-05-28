/*FADD module.
Calculate operand1 + operand2 within error of max(|op1|, |op2|, |op1 + op2|)*2^(-22).
The module omits LSBs of an operand whose magnitude is smaller so that the circuit will be simple.
Inputs:
    op1 (wire): The first operand.
    op2 (wire): The second operand.
Outputs:
    ret (wire): The result of the addition.
*/
module faddmc (
    input clk, resetn,
    input [31:0] op1,
    input [31:0] op2,

    output [31:0] ret
);

    wire [7:0] exp1 = op1[30:23], exp2 = op2[30:23];
    wire [23:0] premanti1 = {1'b1, op1[22:0]}, premanti2 = {1'b1, op2[22:0]};


    // chose the operand to be the augend/minuend, whose magnitude is bigger 
    reg [31:0] op_pre0, op_post;

    always_comb begin
        if (exp1 == exp2) begin
            {op_pre0, op_post} = (premanti1 < premanti2)? {op2, op1}: {op1, op2};
        end else begin
            {op_pre0, op_post} = (exp1 < exp2)? {op2, op1}: {op1, op2};
        end
    end

    wire sig_pre0 = op_pre0[31], sig_post0 = op_post[31];
    wire [7:0] exp_pre0 = op_pre0[30:23], exp_post0 = op_post[30:23];


    // equalize exponents
    wire [9:0] expdiff;

    assign expdiff = {1'b0, exp_pre0} - {1'b0, exp_post0};

    wire [23:0] manti_pre = {1'b1, op_pre0[22:0]};
    wire [23:0] manti_post = {1'b1, op_post[22:0]} >> expdiff;


    // addition, or subtraction
    wire ret_sig0 = sig_pre0;

    wire [24:0] calcbuf0;

    // do addition or subtraction
    assign calcbuf0 = (sig_pre0 == sig_post0)? {1'b0, manti_pre} + {1'b0, manti_post}:
                    {1'b0, manti_pre} - {1'b0, manti_post};


    // split here?
    reg [31:0] op_pre1;
    reg [7:0] exp_pre1, exp_post1;
    reg ret_sig1;
    reg [24:0] calcbuf1;
    reg sig_pre1, sig_post1;

    always_ff @( posedge clk ) begin 
        if (~resetn) begin
            {op_pre1, exp_pre1, exp_post1, ret_sig1, calcbuf1,
                sig_pre1, sig_post1} <= '0;
        end else begin
            {op_pre1, exp_pre1, exp_post1, ret_sig1, calcbuf1,
                sig_pre1, sig_post1}
                <= {op_pre0, exp_pre0, exp_post0, ret_sig0,
                         calcbuf0, sig_pre0, sig_post0};
        end
    end
    
    reg [22:0] ret_manti1;
    reg [7:0] ret_exp1;
    wire [4:0] msbcount1;
    reg [8:0] shamt1, pre_ret_exp1;

    priorityEncoder24_5 enc(calcbuf1[23:0], msbcount1);

    // drive ret_exp1, ret_manti1
    always_comb begin
        shamt1 = '0;
        pre_ret_exp1 = '0;

        if (exp_post1 == '0) begin
            // 2nd operand is 0
            {ret_exp1, ret_manti1} = op_pre1[30:0];
            
        end else if (sig_pre1 == sig_post1) begin
            // addition
            if (calcbuf1[24]) begin
                ret_manti1 = calcbuf1[23:1];
                ret_exp1 = exp_pre1 + 8'b1;
            end else begin
                ret_manti1 = calcbuf1[22:0];
                ret_exp1 = exp_pre1;
            end

        end else begin
            // subtraction
            if (calcbuf1 == '0) begin
                ret_manti1 = '0;
                ret_exp1 = '0;
            end else begin
                shamt1 = 9'd23 - {4'b0, msbcount1};

                if (shamt1 > {1'b0, exp_pre1}) begin
                    ret_manti1 = '0;
                    ret_exp1 = '0;
                end else begin
                    pre_ret_exp1 = {1'b0, exp_pre1} - shamt1;
                    ret_exp1 = pre_ret_exp1[7:0];
                    ret_manti1 = calcbuf1[22:0] << shamt1;
                end
            end
        end
    end


    // return 
    assign ret = {ret_sig1, ret_exp1, ret_manti1};
    
endmodule


/*An priority encoder whose input is 24bits wide.
Used in fadd when subtraction is to be done.
Given an input of 24bits, returns the biggest index i that satisfies input[i] == 1.
Not supposed to be given '0, and when '0 is given, this module returns '0, same as the case
where input is 24'b1.
Inputs:
    data (wire): Non-zero number.
Outputs:
    ret (wire): The index of a highest set bit
*/
module priorityEncoder24_5(
    input wire [23:0] data,

    output wire [4:0] ret
);

    wire [4:0] undefined = 5'd0;

    assign ret = data[23]? 5'd23: 
                data[22]? 5'd22: 
                data[21]? 5'd21: 
                data[20]? 5'd20: 
                data[19]? 5'd19: 
                data[18]? 5'd18: 
                data[17]? 5'd17: 
                data[16]? 5'd16: 
                data[15]? 5'd15: 
                data[14]? 5'd14: 
                data[13]? 5'd13: 
                data[12]? 5'd12: 
                data[11]? 5'd11: 
                data[10]? 5'd10: 
                data[9]? 5'd9: 
                data[8]? 5'd8: 
                data[7]? 5'd7: 
                data[6]? 5'd6: 
                data[5]? 5'd5: 
                data[4]? 5'd4: 
                data[3]? 5'd3: 
                data[2]? 5'd2: 
                data[1]? 5'd1: 
                data[0]? 5'd0: undefined;
    
endmodule