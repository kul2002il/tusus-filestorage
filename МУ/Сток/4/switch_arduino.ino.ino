
// TC1 на 1Гц.
/*

uint16_t frequency = 1;
uint32_t lastButtonChangeTime = 0;

void setup() {
  DDRC = 0;
  DDRB |= 0b111100;

  // Кнопки
  PCICR = 0b010;
  PCMSK1 = 0b1110;
  
  // TC1.
  TIMSK1 = 1;
  TCCR1A = 0b00000000;
  TCCR1B = 0b00000101; // Тактирование с делителем 1024.
  TCNT1 = 65500;
  
  sei();
}

ISR(PCINT1_vect) {
  if (millis() - lastButtonChangeTime < 100) {
    return;
  }

  lastButtonChangeTime = millis();

  if (PINC & 0b0010 && frequency > 1) {
    --frequency;
  }
  if (PINC & 0b0100 && frequency < 100) {
    ++frequency;
  }
}

ISR(TIMER1_OVF_vect) {
  TCNT1 = 65536 - 15626 / frequency;
  
  PORTB ^= 1 << 2;
}



void loop() {
}
//*/






// Программный ШИМ на TC2.
/*

uint8_t light = 100;
uint32_t lastButtonChangeTime = 0;

void setup() {
  DDRC = 0;
  DDRB = 0b111100;
  PORTB = 0b111100;

  // Кнопки
  PCICR = 0b010;
  PCMSK1 = 0b1110;

  // TC2.
  TIMSK2 = (1<<TOIE2) | (1<<OCIE2A);
  TCCR2B = (1 << CS21) | (1 << CS21) | (0 << CS20); // Тактирование с делителем 256.
  OCR2A = 200;
  
  sei();

  Serial.begin(9600);
}

ISR(TIMER2_OVF_vect) {
  PORTB &= ~(1 << 3);
}
ISR(TIMER2_COMPA_vect) {
  PORTB |= 1 << 3;
}

ISR(PCINT1_vect) {
  if (millis() - lastButtonChangeTime < 100) {
    return;
  }

  lastButtonChangeTime = millis();

  if (~PINC & 0b0010) {
    if (light > 20) {
      light -= 20;
    } else {
      light = 20;
    }
  }
  if (~PINC & 0b0100) {
    if (light < 230) {
      light += 20;
    } else {
      light = 254;
    }
  }

  OCR2A = light;
  Serial.println(light);
}

void loop() {
}
//*/





// Аппаратный ШИМ на TC2.
//*

uint8_t light = 100;
uint32_t lastButtonChangeTime = 0;

void setup() {
  DDRC = 0;
  DDRB = 0b111100;
  PORTB = 0b111100;

  // Кнопки
  PCICR = 0b010;
  PCMSK1 = 0b1110;

  // TC2 PWM.
  TCCR2A = (1 << COM2A1) | (0 << COM2A1) | (1 << WGM21) | (1 << WGM20);
  TCCR2B = (0 << WGM22) | (1 << CS21) | (1 << CS21) | (0 << CS20); // Тактирование с делителем 256.
  OCR2A = 100;
  
  sei();
}

ISR(PCINT1_vect) {
  if (millis() - lastButtonChangeTime < 100) {
    return;
  }

  lastButtonChangeTime = millis();

  if (~PINC & 0b0010) {
    if (light > 20) {
      light -= 20;
    } else {
      light = 20;
    }
  }
  if (~PINC & 0b0100) {
    if (light < 230) {
      light += 20;
    } else {
      light = 254;
    }
  }

  OCR2A = light;
}

void loop() {
}
//*/











