# Truth-Table-Generator
Generates truth table for a given boolean expression dynamically

# Usage
- Captial letters act as variables

- Variable names dont need to be consecutive

- Brackets work normally

- spaces dont matter

- logic operators can be capital or small

`not`/`!`: "!A"
`and`/`.`: "A.B" ("AB" does not work)
`or`/`+`: "A+B"
`xor`/`^`: "A^B"

# Examples
`((A and not B) or (B xor C)) and C`<br>
is the same as<br>
`((A.!B)+(B^C)).C`<br>
and<br>
`((Mand!J)OR(J^P)) .P`

# Todos and bugs
- gui resize
- `A xor not B` fix (`A xor (not B)` works tho)
- add `nor` gate
- add `nand` gate