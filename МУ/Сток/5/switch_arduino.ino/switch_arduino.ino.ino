
#define CHAR_NULL 10;

char chars[] = {
  0b11111100, // 0
  0b01100000, // 1
  0b11011010, // 2
  0b11110010, // 3
  0b01100110, // 4
  0b10110110, // 5
  0b10111110, // 6
  0b11100000, // 7
  0b11111110, // 8
  0b11110110, // 9
  0b00000000, // null
};

void sendBit(char data) {
  if (data & 1) {
    PORTB |= 1;
  } else {
    PORTB &= ~1;
  }
  PORTD |= 1<<7;
  PORTD &= ~(1<<7);
}

void sendByte(char data) {
  for (int i = 0; i < 8; i++) {
    sendBit(data);
    data >>= 1;
  }
}

void passNumbers() {
  PORTD |= 1<<4;
  PORTD &= ~(1<<4);
}

char currentChars[4] = {1, 9, 8, 4};

void sendCurrentChar(char index) {
  sendByte(~chars[currentChars[index]]);
  sendByte(1 << (7 - index));
  passNumbers();
}

void setup() {
  DDRB = 0b00000001;
  DDRC = 0b00000000;
  DDRD = 0b10010000;

  // TC2.
  TIMSK2 = (1<<TOIE2);
  TCCR2B = (1 << CS21) | (1 << CS21) | (0 << CS20); // Тактирование с делителем 256.
  OCR2A = 200;
  
  sei();

  Serial.begin(9600);
}

char index = 0;

ISR(TIMER2_OVF_vect) {
  sendCurrentChar(index);
  index = (index + 1) & 0b11;
}

char inputIndex = 0;

void loop() {
  if (Serial.available()) {
    currentChars[0] = CHAR_NULL;
    currentChars[1] = CHAR_NULL;
    currentChars[2] = CHAR_NULL;
    currentChars[3] = CHAR_NULL;
    
    for (int i = 0; i < 4; i++) {
      if (!Serial.available()) {
        break;
      }
      char input = Serial.read();
      if (input < '0' || input > '9') {
        break;
      }
      currentChars[i] = input - '0';
      delay(10);
    }
  }
}






