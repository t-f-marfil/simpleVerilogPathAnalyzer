
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "ALLHIGH ALLLOW ALWAYS ALWAYSCOMB ALWAYSFF ASSIGN BEGIN ELSE END ENDMODULE EQ GEQ ID IF INPUT LEQ LITWIRE LOCALPARAM LOGIC LSHIFT MODULE NEGEDGE NONBLOCK NUMBER OUTPUT PARAMETER POSEDGE REG RSHIFT WIRE\n    source : moduledec source \n           | empty\n    \n    moduledec : MODULE ID paramdec portdec ';' modulecontent ENDMODULE\n              | MODULE ID portdec ';' modulecontent ENDMODULE\n    \n    paramdec : '#' '(' params ')'\n    \n    params : oneparam paramplus \n           | empty\n    \n    paramplus : ',' oneparam paramplus \n              | empty\n    \n    oneparam : PARAMETER ID '=' arithexpr\n    \n    arithexpr : NUMBER\n    \n    portdec : '(' ports ')'\n    \n    ports : oneport portplus \n          | empty\n    \n    portplus : ',' oneport portplus \n             | empty\n    \n    oneport : inouttype ID\n            | inouttype '[' arithexpr ':' arithexpr ']' ID\n    \n    inouttype : INPUT\n              | OUTPUT\n              | INPUT wiretype\n              | OUTPUT wiretype\n    \n    modulecontent : wiredec ';' modulecontent\n                  | assign ';' modulecontent\n                  | always modulecontent\n                  | empty\n    \n    wiredec : wiretype '[' arithexpr ':' arithexpr ']' ID\n            | wiretype ID\n    \n    wiretype : WIRE\n             | REG\n             | LOGIC\n    \n    assign : ASSIGN lhs '=' wireexpr\n    \n    always : ALWAYS '@' sensitivity alwayscontblock\n           | ALWAYSFF '@' sensitivity alwayscontblock\n           | ALWAYSCOMB alwayscontblock\n    \n    sensitivity : '(' edge ID ')'\n    \n    edge : POSEDGE\n         | NEGEDGE\n    \n    alwayscontblock : BEGIN alwayscont END \n    \n    alwayscont : oneassign ';' alwayscont\n               | ifblock alwayscont\n               | ifblock elseblock alwayscont\n               | empty\n    \n    oneassign : lhs '=' wireexpr\n              | lhs NONBLOCK wireexpr\n    \n    ifblock : IF '(' wireexpr ')' BEGIN alwayscont END\n    \n    elseblock : ELSE ifblock\n              | ELSE ifblock elseblock\n              | ELSE BEGIN alwayscont END\n    \n    lhs : ID\n        | ID '[' arithexpr ':' arithexpr ']'\n        | '{' lhsconcat '}'\n    \n    lhsconcat : lhs\n              | lhs ',' lhsconcat\n    \n    wireexpr : wireval\n             | wireval wireop wireexpr\n             | wireval '?' wireexpr ':' wireexpr\n    \n    wireval : ALLHIGH\n            | ALLLOW\n            | LITWIRE\n            | '{' wireconcat '}'\n            | '(' wireexpr ')'\n            | ID '[' arithexpr ':' arithexpr ']'\n            | ID '[' arithexpr ']'\n            | unaop wireval\n    \n    unaop : '~'\n          | '&'\n          | '^'\n          | '|'\n    \n    wireval : ID\n    \n    wireconcat : wireexpr\n               | wireexpr ',' wireconcat\n    \n    wireop : '+'\n           | '-'\n           | '*'\n           | '&'\n           | '|'\n           | '^'\n           | '<'\n           | '>'\n           | EQ\n           | GEQ\n           | LEQ\n    \n    empty : \n    "
    
_lr_action_items = {'MODULE':([0,2,47,68,],[4,4,-4,-3,]),'$end':([0,1,2,3,5,47,68,],[-84,0,-84,-2,-1,-4,-3,]),'ID':([4,17,18,19,26,27,31,32,33,37,44,45,55,59,72,81,95,96,98,99,100,101,102,105,107,108,109,112,114,116,117,118,123,124,125,126,127,128,129,130,131,132,133,134,135,146,147,151,152,156,161,166,171,172,177,],[6,42,-19,-20,52,54,-29,-30,-31,64,-21,-22,54,54,97,54,97,97,97,-66,-67,-68,-69,54,143,-37,-38,54,54,97,97,97,97,97,-73,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,-47,54,164,165,97,-48,97,-49,54,-46,]),'#':([6,],[9,]),'(':([6,7,9,56,57,60,72,84,95,96,98,99,100,101,102,116,117,118,123,124,125,126,127,128,129,130,131,132,133,134,135,156,166,],[10,10,13,77,77,-5,96,118,96,96,96,-66,-67,-68,-69,96,96,96,96,96,-73,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,96,96,]),';':([8,11,22,23,38,52,80,90,91,92,93,94,97,140,148,149,153,155,157,165,169,173,176,],[12,20,48,49,-12,-28,112,-32,-55,-58,-59,-60,-70,-65,-44,-45,-56,-61,-62,-27,-64,-57,-63,]),')':([10,13,14,15,16,34,35,36,39,41,42,61,63,65,67,85,87,91,92,93,94,97,119,120,138,140,143,150,153,155,157,164,169,173,176,],[-84,-84,38,-84,-14,60,-84,-7,-13,-16,-17,-6,-9,-84,-11,-84,-15,-55,-58,-59,-60,-70,-8,-10,157,-65,160,163,-56,-61,-62,-18,-64,-57,-63,]),'INPUT':([10,40,],[18,18,]),'OUTPUT':([10,40,],[19,19,]),'ASSIGN':([12,20,24,48,49,58,106,110,111,],[27,27,27,27,27,-35,-33,-34,-39,]),'ALWAYS':([12,20,24,48,49,58,106,110,111,],[28,28,28,28,28,-35,-33,-34,-39,]),'ALWAYSFF':([12,20,24,48,49,58,106,110,111,],[29,29,29,29,29,-35,-33,-34,-39,]),'ALWAYSCOMB':([12,20,24,48,49,58,106,110,111,],[30,30,30,30,30,-35,-33,-34,-39,]),'ENDMODULE':([12,20,21,24,25,46,48,49,50,58,69,70,106,110,111,],[-84,-84,47,-84,-26,68,-84,-84,-25,-35,-23,-24,-33,-34,-39,]),'WIRE':([12,18,19,20,24,48,49,58,106,110,111,],[31,31,31,31,31,31,31,-35,-33,-34,-39,]),'REG':([12,18,19,20,24,48,49,58,106,110,111,],[32,32,32,32,32,32,32,-35,-33,-34,-39,]),'LOGIC':([12,18,19,20,24,48,49,58,106,110,111,],[33,33,33,33,33,33,33,-35,-33,-34,-39,]),'PARAMETER':([13,62,],[37,37,]),',':([15,35,42,54,65,67,75,85,91,92,93,94,97,104,120,137,140,153,155,157,164,169,170,173,176,],[40,62,-17,-50,40,-11,105,62,-55,-58,-59,-60,-70,-52,-10,156,-65,-56,-61,-62,-18,-64,-51,-57,-63,]),'[':([17,18,19,26,31,32,33,44,45,54,97,],[43,-19,-20,51,-29,-30,-31,-21,-22,73,139,]),'{':([27,55,59,72,81,95,96,98,99,100,101,102,105,112,114,116,117,118,123,124,125,126,127,128,129,130,131,132,133,134,135,146,147,156,161,166,171,172,177,],[55,55,55,95,55,95,95,95,-66,-67,-68,-69,55,55,55,95,95,95,95,95,-73,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,-47,55,95,-48,95,-49,55,-46,]),'@':([28,29,],[56,57,]),'BEGIN':([30,76,78,115,160,163,],[59,59,59,147,-36,172,]),'NUMBER':([43,51,73,86,88,89,139,141,168,],[67,67,67,67,67,67,67,67,67,]),'=':([53,54,64,83,104,170,],[72,-50,86,116,-52,-51,]),'}':([54,74,75,91,92,93,94,97,104,136,137,140,142,153,155,157,167,169,170,173,176,],[-50,104,-53,-55,-58,-59,-60,-70,-52,155,-71,-65,-54,-56,-61,-62,-72,-64,-51,-57,-63,]),'NONBLOCK':([54,83,104,170,],[-50,117,-52,-51,]),'IF':([59,81,112,114,115,146,147,161,171,172,177,],[84,84,84,84,84,-47,84,-48,-49,84,-46,]),'END':([59,79,81,82,112,113,114,144,145,146,147,161,162,171,172,175,177,],[-84,111,-84,-43,-84,-41,-84,-40,-42,-47,-84,-48,171,-49,-84,177,-46,]),':':([66,67,71,91,92,93,94,97,103,140,153,154,155,157,158,169,173,176,],[88,-11,89,-55,-58,-59,-60,-70,141,-65,-56,166,-61,-62,168,-64,-57,-63,]),']':([67,121,122,158,159,174,],[-11,151,152,169,170,176,]),'ALLHIGH':([72,95,96,98,99,100,101,102,116,117,118,123,124,125,126,127,128,129,130,131,132,133,134,135,156,166,],[92,92,92,92,-66,-67,-68,-69,92,92,92,92,92,-73,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,92,92,]),'ALLLOW':([72,95,96,98,99,100,101,102,116,117,118,123,124,125,126,127,128,129,130,131,132,133,134,135,156,166,],[93,93,93,93,-66,-67,-68,-69,93,93,93,93,93,-73,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,93,93,]),'LITWIRE':([72,95,96,98,99,100,101,102,116,117,118,123,124,125,126,127,128,129,130,131,132,133,134,135,156,166,],[94,94,94,94,-66,-67,-68,-69,94,94,94,94,94,-73,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,94,94,]),'~':([72,95,96,98,99,100,101,102,116,117,118,123,124,125,126,127,128,129,130,131,132,133,134,135,156,166,],[99,99,99,99,-66,-67,-68,-69,99,99,99,99,99,-73,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,99,99,]),'&':([72,91,92,93,94,95,96,97,98,99,100,101,102,116,117,118,123,124,125,126,127,128,129,130,131,132,133,134,135,140,155,156,157,166,169,176,],[100,128,-58,-59,-60,100,100,-70,100,-66,-67,-68,-69,100,100,100,100,100,-73,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,-65,-61,100,-62,100,-64,-63,]),'^':([72,91,92,93,94,95,96,97,98,99,100,101,102,116,117,118,123,124,125,126,127,128,129,130,131,132,133,134,135,140,155,156,157,166,169,176,],[101,130,-58,-59,-60,101,101,-70,101,-66,-67,-68,-69,101,101,101,101,101,-73,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,-65,-61,101,-62,101,-64,-63,]),'|':([72,91,92,93,94,95,96,97,98,99,100,101,102,116,117,118,123,124,125,126,127,128,129,130,131,132,133,134,135,140,155,156,157,166,169,176,],[102,129,-58,-59,-60,102,102,-70,102,-66,-67,-68,-69,102,102,102,102,102,-73,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,-65,-61,102,-62,102,-64,-63,]),'POSEDGE':([77,],[108,]),'NEGEDGE':([77,],[109,]),'ELSE':([81,146,177,],[115,115,-46,]),'?':([91,92,93,94,97,140,155,157,169,176,],[124,-58,-59,-60,-70,-65,-61,-62,-64,-63,]),'+':([91,92,93,94,97,140,155,157,169,176,],[125,-58,-59,-60,-70,-65,-61,-62,-64,-63,]),'-':([91,92,93,94,97,140,155,157,169,176,],[126,-58,-59,-60,-70,-65,-61,-62,-64,-63,]),'*':([91,92,93,94,97,140,155,157,169,176,],[127,-58,-59,-60,-70,-65,-61,-62,-64,-63,]),'<':([91,92,93,94,97,140,155,157,169,176,],[131,-58,-59,-60,-70,-65,-61,-62,-64,-63,]),'>':([91,92,93,94,97,140,155,157,169,176,],[132,-58,-59,-60,-70,-65,-61,-62,-64,-63,]),'EQ':([91,92,93,94,97,140,155,157,169,176,],[133,-58,-59,-60,-70,-65,-61,-62,-64,-63,]),'GEQ':([91,92,93,94,97,140,155,157,169,176,],[134,-58,-59,-60,-70,-65,-61,-62,-64,-63,]),'LEQ':([91,92,93,94,97,140,155,157,169,176,],[135,-58,-59,-60,-70,-65,-61,-62,-64,-63,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'source':([0,2,],[1,5,]),'moduledec':([0,2,],[2,2,]),'empty':([0,2,10,12,13,15,20,24,35,48,49,59,65,81,85,112,114,147,172,],[3,3,16,25,36,41,25,25,63,25,25,82,41,82,63,82,82,82,82,]),'paramdec':([6,],[7,]),'portdec':([6,7,],[8,11,]),'ports':([10,],[14,]),'oneport':([10,40,],[15,65,]),'inouttype':([10,40,],[17,17,]),'modulecontent':([12,20,24,48,49,],[21,46,50,69,70,]),'wiredec':([12,20,24,48,49,],[22,22,22,22,22,]),'assign':([12,20,24,48,49,],[23,23,23,23,23,]),'always':([12,20,24,48,49,],[24,24,24,24,24,]),'wiretype':([12,18,19,20,24,48,49,],[26,44,45,26,26,26,26,]),'params':([13,],[34,]),'oneparam':([13,62,],[35,85,]),'portplus':([15,65,],[39,87,]),'lhs':([27,55,59,81,105,112,114,147,172,],[53,75,83,83,75,83,83,83,83,]),'alwayscontblock':([30,76,78,],[58,106,110,]),'paramplus':([35,85,],[61,119,]),'arithexpr':([43,51,73,86,88,89,139,141,168,],[66,71,103,120,121,122,158,159,174,]),'lhsconcat':([55,105,],[74,142,]),'sensitivity':([56,57,],[76,78,]),'alwayscont':([59,81,112,114,147,172,],[79,113,144,145,162,175,]),'oneassign':([59,81,112,114,147,172,],[80,80,80,80,80,80,]),'ifblock':([59,81,112,114,115,147,172,],[81,81,81,81,146,81,81,]),'wireexpr':([72,95,96,116,117,118,123,124,156,166,],[90,137,138,148,149,150,153,154,137,173,]),'wireval':([72,95,96,98,116,117,118,123,124,156,166,],[91,91,91,140,91,91,91,91,91,91,91,]),'unaop':([72,95,96,98,116,117,118,123,124,156,166,],[98,98,98,98,98,98,98,98,98,98,98,]),'edge':([77,],[107,]),'elseblock':([81,146,],[114,161,]),'wireop':([91,],[123,]),'wireconcat':([95,156,],[136,167,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> source","S'",1,None,None,None),
  ('source -> moduledec source','source',2,'p_source','svyacc.py',13),
  ('source -> empty','source',1,'p_source','svyacc.py',14),
  ('moduledec -> MODULE ID paramdec portdec ; modulecontent ENDMODULE','moduledec',7,'p_moduledec','svyacc.py',27),
  ('moduledec -> MODULE ID portdec ; modulecontent ENDMODULE','moduledec',6,'p_moduledec','svyacc.py',28),
  ('paramdec -> # ( params )','paramdec',4,'p_paramdec','svyacc.py',43),
  ('params -> oneparam paramplus','params',2,'p_params','svyacc.py',51),
  ('params -> empty','params',1,'p_params','svyacc.py',52),
  ('paramplus -> , oneparam paramplus','paramplus',3,'p_paramplus','svyacc.py',65),
  ('paramplus -> empty','paramplus',1,'p_paramplus','svyacc.py',66),
  ('oneparam -> PARAMETER ID = arithexpr','oneparam',4,'p_oneparam','svyacc.py',79),
  ('arithexpr -> NUMBER','arithexpr',1,'p_arithexpr','svyacc.py',87),
  ('portdec -> ( ports )','portdec',3,'p_portdec','svyacc.py',95),
  ('ports -> oneport portplus','ports',2,'p_ports','svyacc.py',103),
  ('ports -> empty','ports',1,'p_ports','svyacc.py',104),
  ('portplus -> , oneport portplus','portplus',3,'p_portplus','svyacc.py',113),
  ('portplus -> empty','portplus',1,'p_portplus','svyacc.py',114),
  ('oneport -> inouttype ID','oneport',2,'p_oneport','svyacc.py',123),
  ('oneport -> inouttype [ arithexpr : arithexpr ] ID','oneport',7,'p_oneport','svyacc.py',124),
  ('inouttype -> INPUT','inouttype',1,'p_inouttype','svyacc.py',136),
  ('inouttype -> OUTPUT','inouttype',1,'p_inouttype','svyacc.py',137),
  ('inouttype -> INPUT wiretype','inouttype',2,'p_inouttype','svyacc.py',138),
  ('inouttype -> OUTPUT wiretype','inouttype',2,'p_inouttype','svyacc.py',139),
  ('modulecontent -> wiredec ; modulecontent','modulecontent',3,'p_modulecontent','svyacc.py',151),
  ('modulecontent -> assign ; modulecontent','modulecontent',3,'p_modulecontent','svyacc.py',152),
  ('modulecontent -> always modulecontent','modulecontent',2,'p_modulecontent','svyacc.py',153),
  ('modulecontent -> empty','modulecontent',1,'p_modulecontent','svyacc.py',154),
  ('wiredec -> wiretype [ arithexpr : arithexpr ] ID','wiredec',7,'p_wiredec','svyacc.py',169),
  ('wiredec -> wiretype ID','wiredec',2,'p_wiredec','svyacc.py',170),
  ('wiretype -> WIRE','wiretype',1,'p_wiretype','svyacc.py',180),
  ('wiretype -> REG','wiretype',1,'p_wiretype','svyacc.py',181),
  ('wiretype -> LOGIC','wiretype',1,'p_wiretype','svyacc.py',182),
  ('assign -> ASSIGN lhs = wireexpr','assign',4,'p_assign','svyacc.py',190),
  ('always -> ALWAYS @ sensitivity alwayscontblock','always',4,'p_always','svyacc.py',198),
  ('always -> ALWAYSFF @ sensitivity alwayscontblock','always',4,'p_always','svyacc.py',199),
  ('always -> ALWAYSCOMB alwayscontblock','always',2,'p_always','svyacc.py',200),
  ('sensitivity -> ( edge ID )','sensitivity',4,'p_sensitivity','svyacc.py',213),
  ('edge -> POSEDGE','edge',1,'p_edge','svyacc.py',220),
  ('edge -> NEGEDGE','edge',1,'p_edge','svyacc.py',221),
  ('alwayscontblock -> BEGIN alwayscont END','alwayscontblock',3,'p_alwayscontblock','svyacc.py',229),
  ('alwayscont -> oneassign ; alwayscont','alwayscont',3,'p_alwayscont','svyacc.py',236),
  ('alwayscont -> ifblock alwayscont','alwayscont',2,'p_alwayscont','svyacc.py',237),
  ('alwayscont -> ifblock elseblock alwayscont','alwayscont',3,'p_alwayscont','svyacc.py',238),
  ('alwayscont -> empty','alwayscont',1,'p_alwayscont','svyacc.py',239),
  ('oneassign -> lhs = wireexpr','oneassign',3,'p_oneassign','svyacc.py',256),
  ('oneassign -> lhs NONBLOCK wireexpr','oneassign',3,'p_oneassign','svyacc.py',257),
  ('ifblock -> IF ( wireexpr ) BEGIN alwayscont END','ifblock',7,'p_ifblock','svyacc.py',268),
  ('elseblock -> ELSE ifblock','elseblock',2,'p_elseblock','svyacc.py',275),
  ('elseblock -> ELSE ifblock elseblock','elseblock',3,'p_elseblock','svyacc.py',276),
  ('elseblock -> ELSE BEGIN alwayscont END','elseblock',4,'p_elseblock','svyacc.py',277),
  ('lhs -> ID','lhs',1,'p_lhs','svyacc.py',294),
  ('lhs -> ID [ arithexpr : arithexpr ]','lhs',6,'p_lhs','svyacc.py',295),
  ('lhs -> { lhsconcat }','lhs',3,'p_lhs','svyacc.py',296),
  ('lhsconcat -> lhs','lhsconcat',1,'p_lhsconat','svyacc.py',310),
  ('lhsconcat -> lhs , lhsconcat','lhsconcat',3,'p_lhsconat','svyacc.py',311),
  ('wireexpr -> wireval','wireexpr',1,'p_wireexpr','svyacc.py',323),
  ('wireexpr -> wireval wireop wireexpr','wireexpr',3,'p_wireexpr','svyacc.py',324),
  ('wireexpr -> wireval ? wireexpr : wireexpr','wireexpr',5,'p_wireexpr','svyacc.py',325),
  ('wireval -> ALLHIGH','wireval',1,'p_wireval_0','svyacc.py',339),
  ('wireval -> ALLLOW','wireval',1,'p_wireval_0','svyacc.py',340),
  ('wireval -> LITWIRE','wireval',1,'p_wireval_0','svyacc.py',341),
  ('wireval -> { wireconcat }','wireval',3,'p_wireval_0','svyacc.py',342),
  ('wireval -> ( wireexpr )','wireval',3,'p_wireval_0','svyacc.py',343),
  ('wireval -> ID [ arithexpr : arithexpr ]','wireval',6,'p_wireval_0','svyacc.py',344),
  ('wireval -> ID [ arithexpr ]','wireval',4,'p_wireval_0','svyacc.py',345),
  ('wireval -> unaop wireval','wireval',2,'p_wireval_0','svyacc.py',346),
  ('unaop -> ~','unaop',1,'p_unaop','svyacc.py',365),
  ('unaop -> &','unaop',1,'p_unaop','svyacc.py',366),
  ('unaop -> ^','unaop',1,'p_unaop','svyacc.py',367),
  ('unaop -> |','unaop',1,'p_unaop','svyacc.py',368),
  ('wireval -> ID','wireval',1,'p_wireval_1','svyacc.py',375),
  ('wireconcat -> wireexpr','wireconcat',1,'p_wireconcat','svyacc.py',383),
  ('wireconcat -> wireexpr , wireconcat','wireconcat',3,'p_wireconcat','svyacc.py',384),
  ('wireop -> +','wireop',1,'p_wireop','svyacc.py',395),
  ('wireop -> -','wireop',1,'p_wireop','svyacc.py',396),
  ('wireop -> *','wireop',1,'p_wireop','svyacc.py',397),
  ('wireop -> &','wireop',1,'p_wireop','svyacc.py',398),
  ('wireop -> |','wireop',1,'p_wireop','svyacc.py',399),
  ('wireop -> ^','wireop',1,'p_wireop','svyacc.py',400),
  ('wireop -> <','wireop',1,'p_wireop','svyacc.py',401),
  ('wireop -> >','wireop',1,'p_wireop','svyacc.py',402),
  ('wireop -> EQ','wireop',1,'p_wireop','svyacc.py',403),
  ('wireop -> GEQ','wireop',1,'p_wireop','svyacc.py',404),
  ('wireop -> LEQ','wireop',1,'p_wireop','svyacc.py',405),
  ('empty -> <empty>','empty',0,'p_empty','svyacc.py',413),
]
