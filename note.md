+ localparam, インスタンス宣言はyaccで解析して、Noneを返す
+ コメント（ramstyleとか）はlexで捨てる
+ arithexpr型は消滅しました（全部wireexpr）

+ ifの条件をwireexprと別のクラスにしたい　
+ 演算子優先度どうなってる(+-*あたり)？
+ for文をすべて捨てている