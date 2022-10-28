
//Variables.
int cpuValue = 0;
int myValues[10]={0,0,0,0,0,0,0,0,0,0};
String action = "0";
int Duration = 0;
int action_pin = 0; 
unsigned long startTime =0;
String strArr[3]; //Set the size of the array to equal the number of values you will be receiveing.
unsigned long current_time = 0;


// Debugging switches and macros
#define DEBUG 0 // Switch debug output on and off by 1 or 0

#if DEBUG
#define PRINTS(s)   { Serial.print(F(s)); }
#define PRINT(s,v)  { Serial.print(F(s)); Serial.print(v); }
#define PRINTX(s,v) { Serial.print(F(s)); Serial.print(F("0x")); Serial.print(v, HEX); }
#else
#define PRINTS(s)
#define PRINT(s,v)
#define PRINTX(s,v)
#endif

void setup()
{
    //Start serial.
    Serial.begin(9600);
    PRINTS("\nStart");
    pinMode(3, INPUT_PULLUP);
    pinMode(4, INPUT_PULLUP);
    pinMode(5, INPUT_PULLUP);
    pinMode(10, OUTPUT);
    pinMode(11, OUTPUT);
    pinMode(12, OUTPUT);
    pinMode(13, OUTPUT);
}


void empty_values() {
  for (int i =0; i < 10;i++){
    myValues[i]=0;
  }
}

int read_inv(int pin){
  if(digitalRead(3)==1){
    return 0;
  }
  else{
    return 1;
  }
}

void loop()
{
  String rxString = "";
  if (Serial.available()) {
      PRINTS("\nStart Serial");
    //Keep looping until there is something in the buffer.
    while (Serial.available()) {
        //Delay to allow byte to arrive in input buffer.
        delay(2);
        //Read a single character from the buffer.
        char ch = Serial.read();
        //Append that single character to a string.
        rxString += ch;
    }
    int stringStart = 0;
    int arrayIndex = 0;
    int last_comma =0;
    PRINT("\n rxString:", rxString);
    for (int i = 0; i  < rxString.length(); i++) {
      //Get character and check if it's our "special" character.
      if (rxString.charAt(i) == ',' ) {
          //Clear previous values from array.
          strArr[arrayIndex] = "";
          //Save substring into array.
          strArr[arrayIndex] = rxString.substring(stringStart, i);
          //Set new string starting point.
          stringStart = (i + 1);
          arrayIndex++;
          last_comma = i;
      }
    }
    strArr[arrayIndex] = "";
    strArr[arrayIndex] = rxString.substring(last_comma+1, rxString.length()-1);

    //Put values from the array into the variables.
    action = strArr[0];
    action_pin = strArr[1].toInt();
    Duration = strArr[2].toInt()*1000;
    int i=0;
    PRINTS("\nArray");
    for (String element : strArr){ // for each element in the array
      PRINT("[", i);
      PRINT(":", element);
      PRINTS("]");      
      i++;
    }
    //start timeer    
    if (action=="d"){
        PRINT("\n activating:", action_pin);
        startTime = millis(); 
        PRINT("\n SET counter:",  startTime); 
    }
  //UPDATE SYSTEM
  }
  //PRINT("\n Perfomring:", action);
  //get values from array and return
  if (action == "q"){
    Serial.write("{");
    for (int i =0; i < 10;i++){
      if(myValues[i]>0){
        //s = "{"muffin" : "olz", "foo" : "kitty'}"
        Serial.write("\"");  
        Serial.print(i);  
        Serial.write("\"");  
        Serial.write(" ");  
        Serial.write(":");  
        Serial.write(" ");  
        Serial.write("\"");  
        Serial.print(myValues[i]);  
        Serial.write("\"");  
      }   
    }
    Serial.write("}"); 
    Serial.write("\n");
    empty_values();
    action ="";
  }
  if (action == "d"){
    PRINT("\n counter:",startTime)
    PRINT("\n Time Remain:",millis() - startTime)
    PRINT("\n Length:",Duration)
    if (millis() - startTime <= Duration){
      digitalWrite(action_pin, 1);
      PRINT("\n on:",action_pin);
    }
    else{
      digitalWrite(action_pin, 0);
      action = '\0';
      PRINT("\n off:",action_pin);
    }
  }
  else{
    //PRINT("why:",action);
  }
  //perform action based on input
  
  myValues[3]= read_inv(3);
  myValues[4]= read_inv(4);
  myValues[5]= read_inv(5);
  

  
  delay(1);
}