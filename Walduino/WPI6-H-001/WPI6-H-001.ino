//Walden Modular Equipment
//2020
//WPI

#include <ResponsiveAnalogRead.h>

int Umbral = 800;
int INB1 = 0;
int INB2 = 0;
int INB3 = 0;
int INB4 = 0;
int INB5 = 0;
int INB6 = 0;

ResponsiveAnalogRead IN1(A0, true);
ResponsiveAnalogRead IN2(A1, true);
ResponsiveAnalogRead IN3(A2, true);
ResponsiveAnalogRead IN4(A3, true);
ResponsiveAnalogRead IN5(A4, true);
ResponsiveAnalogRead IN6(A5, true);

int ReadSerial = '0';
int AB = 2;
int CD = 3;
int EF = 4;
int GH = 5;
int IJ = 6;
int KL = 7;

void setup() 
{
  Serial.begin(9600);
  pinMode(AB, OUTPUT); 
  pinMode(CD, OUTPUT); 
  pinMode(EF, OUTPUT); 
  pinMode(GH, OUTPUT); 
  pinMode(IJ, OUTPUT); 
  pinMode(KL, OUTPUT); 
}

void loop() 
{
  IN1.update();
  IN2.update();
  IN3.update();
  IN4.update();
  IN5.update();
  IN6.update();

  Serial.print(INB1);
  Serial.print(INB2);
  Serial.print(INB3);
  Serial.print(INB4);
  Serial.print(INB5);
  Serial.print(INB6);

  if (IN1.getValue() >= Umbral)
  {
    INB1 = 1;
  }
  else
  {
    INB1 = 0;
  }
  
  if (IN2.getValue() >= Umbral)
  {
    INB2 = 1;
  }
  else
  {
    INB2 = 0;
  }
  
  if (IN3.getValue() >= Umbral)
  {
    INB3 = 1;
  }
  else
  {
    INB3 = 0;
  }
  
  if (IN4.getValue() >= Umbral)
  {
    INB4 = 1;
  }
  else
  {
    INB4 = 0;
  }
  
  if (IN5.getValue() >= Umbral)
  {
    INB5 = 1;
  }
  else
  {
    INB5 = 0;
  }
  
  if (IN6.getValue() >= Umbral)
  {
    INB6 = 1;
  }
  else
  {
    INB6 = 0;
  }
  
  if (Serial.available() > 0)
  {
    ReadSerial = Serial.read();
    
        if(ReadSerial == 'a')
        {
          digitalWrite(AB,1);
        }
        else if(ReadSerial == 'b')
        {
          digitalWrite(AB,0);
        }   
        
        if(ReadSerial == 'c')
        {
          digitalWrite(CD,1);
        }
        else if(ReadSerial == 'd')
        {
          digitalWrite(CD,0);
        }  
        
        if(ReadSerial == 'e')
        {
          digitalWrite(EF,1);
        }
        else if(ReadSerial == 'f')
        {
          digitalWrite(EF,0);
        } 
        
        if(ReadSerial == 'g')
        {
          digitalWrite(GH,1);
        }
        else if(ReadSerial == 'h')
        {
          digitalWrite(GH,0);
        } 
        
        if(ReadSerial == 'i')
        {
          digitalWrite(IJ,1);
        }
        else if(ReadSerial == 'j')
        {
          digitalWrite(IJ,0);
        } 
        
        if(ReadSerial == 'k')
        {
          digitalWrite(KL,1);
        }
        else if(ReadSerial == 'l')
        {
          digitalWrite(KL,0);
        } 
  }
  
  delay(100);
}
