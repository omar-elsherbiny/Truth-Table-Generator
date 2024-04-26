# Truth-Table-Generator
Generates truth table for a given boolean expression dynamically

I added a compiled version for easy setup :)

# Usage
- Captial letters act as variables

- Variable names dont need to be consecutive

- Brackets work normally

- spaces dont matter

- logic operators can be capital or small

- variables are ordered alphabetically in grid

`not` / `!` : "!A"<br>
`and` / `.` : "A.B" ("AB" does not work)<br>
`or` / `+` : "A+B"<br>
`xor` / `^` : "A^B", "A xor (not B)"<br>
`nor` : "(A)nor(B)"<br>
`nand` : (A)nand(B)"<br>

*brackets on operands are required in `nor`, `nand` and with `xor` if it has a `not` operand

# Examples
`((A and not B) or (B xor C)) and C`<br>
is the same as<br>
`((A.!B)+(B^C)).C`<br>
and<br>
`((Mand!J)OR(J^P)) .P`<br><br>
`((A + B) nand ((C) nor (D)))`

# Todos and bugs
- none till now :>
