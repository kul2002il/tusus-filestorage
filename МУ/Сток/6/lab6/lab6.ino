
#define SHR_SDI PB0
#define SHR_CLK PD7
#define SHR_LCHCLK PD4
#define SHR_DDRDATA DDRB
#define SHR_DDRCLK DDRD
#define SHR_PORTDATA PORTB
#define SHR_PORTCLK PORTD
#define SHR_DELAY 0
void SHRSetup()
{
 SHR_DDRDATA|=1<<SHR_SDI;
 SHR_DDRCLK|=1<<SHR_CLK;
 SHR_DDRCLK|=1<<SHR_LCHCLK;
 SHR_PORTDATA&=~(1<<SHR_SDI);
 SHR_PORTCLK&=~(1<<SHR_CLK);
 SHR_PORTCLK&=~(1<<SHR_LCHCLK);
}
void SHRSendBit(int bit)
{
 SHR_PORTDATA|=bit<<SHR_SDI;
 SHR_PORTCLK|=1<<SHR_CLK;
 SHR_PORTDATA&=~(bit<<SHR_SDI);
 SHR_PORTCLK&=~(1<<SHR_CLK);
}
void SHRSendByte(byte data)
{
 for(int i=0;i<8;++i)
 SHRSendBit((data&(1<<(7-i)))>>(7-i));
}
void SHRSendLatch()
{
 SHR_PORTCLK|=1<<SHR_LCHCLK;
 SHR_PORTCLK&=~(1<<SHR_LCHCLK);
}
void SHRSendSymb(int num,bool isDot)
{
 static char table[10]={127&~(1<<6),//0
 (1<<2)|(1<<1),//1
 (1<<6)|(1<<4)|(1<<3)|(1<<1)|(1<<0),//2
 (1<<6)|(1<<3)|(1<<2)|(1<<1)|(1<<0),//3
 (1<<6)|(1<<5)|(1<<2)|(1<<1),//4
 (1<<6)|(1<<5)|(1<<3)|(1<<2)|(1<<0),//5
 (1<<6)|(1<<5)|(1<<4)|(1<<3)|(1<<2)|(1<<0),//6
 (1<<2)|(1<<1)|(1<<0),//7
 127,
 127&~(1<<4)
 };
 int dot=(isDot<<7);
 SHRSendByte(~(table[num]|dot));
}
void SHRSelectSegment(int num)
{
 SHRSendByte(1<<num);
}
void SHRSendNum(float num)
{
 float tmp=1000;
 int numAfterPoint=0;
 while((tmp>num)&&(tmp>1))
 {
 tmp/=10;
 numAfterPoint++;
 }
 int numBeforePoint=4-numAfterPoint;
 for(int i=0;i<numAfterPoint;++i)
 num*=10;
 int intNum=num;
 int num4=intNum%10;
 intNum/=10;
 int num3=intNum%10;
 intNum/=10;
 int num2=intNum%10;
 intNum/=10;
 int num1=intNum%10;
 SHRSendSymb(num1,(numBeforePoint==1));
 SHRSelectSegment(0);
 SHRSendLatch();
 SHRSendSymb(num2,(numBeforePoint==2));
 SHRSelectSegment(1);
 SHRSendLatch();
 SHRSendSymb(num3,(numBeforePoint==3));
 SHRSelectSegment(2);
 SHRSendLatch();
 SHRSendSymb(num4,false);
 SHRSelectSegment(3);
 SHRSendLatch();
}
void setup()
{
 SHRSetup();

  ADMUX = 0b01000000; // Питание от AVCC и считывание ADC0.
  ADCSRA = (1 << ADEN) // Включение.
    | (1 << ADSC) // Старт преобразования
    | (1 << ADATE) // Постоянное преобразование.
    | (1 << ADIE) // Включение прерывания.
    | 0b111; // Предделитель на 128.
  DIDR0 = 1 << 0; // Отключить пин ADC0 от цифровой части.
}

float valADC = 0;

void loop()
{
 SHRSendNum(valADC);
}

ISR(ADC_vect){
  valADC = ADC * 5.0f / 1024;
}
