##Calculator

CircuitPython calculator firmware for a Feather RP2040 with DVI output, driven by a 5x4 matrix keypad.
 
## Hardware
 
- Adafruit Feather RP2040 DVI 
- 5x4 matrix keypad, diodes pointing toward the columns (cathode at column, anode at row)
- HDMI/DVI display — tested target is a 7" 1024x600 panel, driven at 800x480 (panel scales it down)
- 
## Keymap
 
```
x      ^      √      ÷
7      8      9      X
4      5      6      -
1      2      3      +
clear  0      .      sum
```
 
(`√` and `÷` show as the real symbols on-screen via the custom font which a extraction of the baisic one to preserve memory)

## Usage
 
**Basic math** — type a number, an operator, another number, then `sum` to evaluate. Chained expressions evaluate left to right
**`x` as a variable**
- `x 3 sum` → stores `3` into `x` (the screen shows `x=3`)
- `x + 5 sum` → substitutes the stored value of `x` into the expression
- Pressing `x` with nothing stored yet and using it in a calc shows an `x undef` error
**`√` (root)** — binary, first number is the degree, second is the radicand: `2 √ 9 sum` → `3` (square root of 9). `3 √ 27 sum` → cube root of 27.
 
**`clear`**
- single press → clears the current entry/expression only
- triple press within ~0.6s → also wipes the stored `x` value (shows `mem cleared`)

##Case
I dint yet make the display part of the case as im planning to do tht after i get it



- <img width="1358" height="887" alt="image" src="https://github.com/user-attachments/assets/7970faff-ff9e-44f4-a9b9-cc3b9c40e8d1" />

<img width="1493" height="595" alt="image" src="https://github.com/user-attachments/assets/bb461423-c564-4fbb-855a-99343c13546c" />


<img width="810" height="492" alt="image" src="https://github.com/user-attachments/assets/aaab2eb1-7696-402c-9f39-0b95c99a34d0" />

<img width="420" height="436" alt="image" src="https://github.com/user-attachments/assets/8d29fab9-bfd3-4df7-8478-2c0392b14bd9" />


