#include <SFE_BMP180.h>
#include <Wire.h>
#include <dht.h>
#include <LiquidCrystal_I2C.h>

SFE_BMP180 pressure;
dht DHT;
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

#define ALTITUDE 49.0 // Altitude of my house ub Howick

#define DHT11_PIN 7 //Pin for Humidity/temperature sensor as it isn't I2C


void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);

  // Initialize the sensor (it is important to get calibration values stored on the device).
  if (!pressure.begin())
    // Oops, something went wrong, this is usually a connection problem,
    //Serial.println("BMP180 init fail\n\n");
    while(1); // Pause forever.

  //time delays so that the first reading is taken just past 12AM (Midnight)
  delay(60UL * 60UL * 1000UL);
  delay(60UL * 60UL * 1000UL);
  delay(20UL * 60UL * 1000UL);
}

void loop() {
  char status;
  double T,P,p0;
  int check = DHT.read11(DHT11_PIN);

  Serial.print("H:");
  Serial.println(DHT.humidity);

  //display humidity to LCD
  //lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("H=");
  lcd.print(DHT.humidity);
  lcd.setCursor(4, 0);
  lcd.print("%  ");


  status = pressure.startTemperature();
  if (status != 0)
  {
    // Wait for the measurement to complete:
    delay(status);

    // Retrieve the completed temperature measurement:
    // Note that the measurement is stored in the variable T.
    // Function returns 1 if successful, 0 if failure.

    status = pressure.getTemperature(T);
    if (status != 0)
    {

      lcd.setCursor(0, 1);
      lcd.print("T=");
      lcd.print(T,2);
      lcd.print("C  ");
      lcd.print((9.0/5.0)*T+32.0,2);
      lcd.print("F");
      
      // Start a pressure measurement:
      // The parameter is the oversampling setting, from 0 to 3 (highest res, longest wait).
      // If request is successful, the number of ms to wait is returned.
      // If request is unsuccessful, 0 is returned.

      status = pressure.startPressure(3);
      if (status != 0)
      {
        // Wait for the measurement to complete:
        delay(status);

        // Retrieve the completed pressure measurement:
        // Note that the measurement is stored in the variable P.
        // Note also that the function requires the previous temperature measurement (T).
        // (If temperature is stable, you can do one temperature measurement for a number of pressure measurements.)
        // Function returns 1 if successful, 0 if failure.

        status = pressure.getPressure(P,T);
        if (status != 0)
        {

          // The pressure sensor returns abolute pressure, which varies with altitude.
          // To remove the effects of altitude, use the sealevel function and your current altitude.
          // This number is commonly used in weather reports.
          // Parameters: P = absolute pressure in mb, ALTITUDE = current altitude in m.
          // Result: p0 = sea-level compensated pressure in mb

          p0 = pressure.sealevel(P,ALTITUDE); // I'm at 49 meters (Howick, Auckland)
          //Serial.print("The relative (sea-level) pressure is: ");
          Serial.print("P:");
          Serial.println(p0,2);

          lcd.setCursor(7,0);
          lcd.print("P=");
          lcd.print(p0*0.0295333727,2);
          lcd.print("Hg");

          Serial.print("F:");
          Serial.println((9.0/5.0)*T+32.0,2);
          Serial.print("C:");
          Serial.println(T,2);
        }
        else Serial.println("error retrieving pressure measurement\n");
      }
      else Serial.println("error starting pressure measurement\n");
    }
    else Serial.println("error retrieving temperature measurement\n");
  }
  else Serial.println("error starting temperature measurement\n");

  delay(60UL * 60UL * 1000UL);
}
