/**
   Mote.pde - Data visualization for motes.
*/

import java.net.*;
import controlP5.*;
import peasy.*;
import processing.opengl.*;

// Networking
int port = 9002;
String host = "127.0.0.1"; // Default to localhost
Socket socket;
InputStream input;
OutputStream output;

// Interface
PeasyCam cam;
PMatrix3D currCameraMatrix;
PGraphics3D g3;
ControlP5 controlP5;
int HIDE_OTHER = 1023; // Constant for hiding non-highlighted series.
RadioButton hide_button;
Textfield address_field;
Numberbox port_field;

// Data
int[][] data = new int[100][10];
float y_scale = 0.05;
color color1 = color(204, 102, 0);
color color2 = color(255, 255, 255);
color bg_color = color(33, 33, 33);
int colorized_series = 0;
int[] data_colors = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
boolean hide_others = false;

/**
   Runs once to set up environment.
 */
void setup(){
  //  size(screen.width, screen.height, OPENGL);
  size(1024, 768, OPENGL);
  g3 = (PGraphics3D) g;
  cam = new PeasyCam(this, 100);
  background(bg_color);
  controlP5 = new ControlP5(this);
  controlP5.setAutoDraw(false);
  int start_x = 100;
  int start_y = 160;
  address_field = controlP5.addTextfield("address", start_x, start_y, 140, 20);
  address_field.setText("127.0.0.1");
  port_field = controlP5.addNumberbox("port", port, start_x + 175, start_y, 70, 20);
  controlP5.addButton("connect", 1, start_x + 280, start_y, 70, 20);
}

/**
   Loop to draw the interface and data
 */
void draw(){
  // Wait for connection to proceed.
  hint(ENABLE_DEPTH_TEST);
  if(socket != null){
    drawData();
  }
  hint(DISABLE_DEPTH_TEST);
  drawGui();
}

/**
   Tweaks to get the gui to draw well.
 */
void drawGui(){
  currCameraMatrix = new PMatrix3D(g3.camera);
  camera();
  controlP5.draw();
  g3.camera = currCameraMatrix;
}

/**
   Draw the data in 3-Space.
 */
void drawData(){
  background(bg_color);
  grabData();
  for(int i = 0; i < data.length; i++){
    for(int j = 0; j < 10; j++){
      // Colorize
      if(data_colors[j] == 1){
        if(hide_others){
          stroke(bg_color);
        } else {
          stroke(color1);      
        }
      } else {
        stroke(color2);      
      }
      // Negate the y to flip upright.
      point(i-50, -(y_scale * data[i][j]) / 100, j-5); 
    }
  }
}

/**
   Handle UI events.
 */
void controlEvent(ControlEvent ev){
  if(ev.isController()){
    Controller controller = ev.controller();
    if(controller.name().equals("connect")){
      host = address_field.getText();
      port = (int) port_field.value();
      print("Connecting to " + host + ":" + port);
      connect(host, port);
    } else if(controller.name().equals("exit")){
      if(socket != null){
        try{
          input.close();
          output.close();
          socket.shutdownInput();
          socket.shutdownOutput();
          socket.close();
        } catch(Exception e){
          // Do nothing.
        }
        exit(); // Let processing do its post-exit hooks.
      }
    }
  }
  else {
    int series = (int) ev.group().value();
    if(series != -1){ // Selection event.
      if(series == HIDE_OTHER){ // Selected to hide other series.
        hide_others = true;
      } else { // Selected a highlight series.
        data_colors[colorized_series] = 1;
        data_colors[series] = 2;
        colorized_series = series;
      }
    } else { // When any radio button is turned off, we get -1.
      if(!hide_button.getState(0) && hide_others){ // Check to see if we got the hide_button.
        hide_others = false;
        //data_colors[colorized_series] = 2; // Set the old series to be on.
      } else {
        data_colors[colorized_series] = 1;
      }
    }
  }
}

/**
   Create the UI.
*/
void generateInterface(){
  controlP5.addTextlabel("onlineField", "We're online... receiving data.",
                         100, 100);
  controlP5.addTextlabel("highlightField", "Highlight",
                         300, 100);
  RadioButton highl_r = controlP5.addRadioButton("highlightButton", 300, 120);
  highl_r.setItemsPerRow(10);
  highl_r.setSpacingColumn(25);
  for(int i = 0; i < 10; i++){
    Toggle t = highl_r.addItem(Integer.toString(i), i);
    t.captionLabel().setColorBackground(color(80));
    t.captionLabel().style().movePadding(2, 0, -1, 2);
    t.captionLabel().style().moveMargin(-2, 0, 0, -3);
    t.captionLabel().style().backgroundWidth = 20;
  }

  highl_r.setItemsPerRow(10);
  highl_r.setSpacingColumn(25);

  hide_button = controlP5.addRadioButton("hideButton", 300, 160);
  Toggle t = hide_button.addItem("Hide others", HIDE_OTHER);
  t.captionLabel().setColorBackground(color(80));
  t.captionLabel().style().movePadding(2, 0, -1, 2);
  t.captionLabel().style().moveMargin(-2, 0, 0, -3);
  t.captionLabel().style().backgroundWidth = 100;
   
  Numberbox nb = controlP5.addNumberbox("y_scale", 0.05, 100, 120, 70, 20);
  nb.setMultiplier(-0.05);

  controlP5.addButton("exit", 1, width - 200, 50, 60, 20);  
}

/**
   Get data from the server.
*/
void grabData(){
  byte[] buffer = new byte[36];
  for(int i = 0; i < 10; i++){
    try{
      if(input.available() < 36){
        if(input.available() > 0){
          println("Available data greater than zero; may have faulty input.");
        }
        break;
      }
      else{
        input.read(buffer);
        byte node = buffer[4];
        // Read out the data into our preallocated buffer.
        for(int j = 0; j < 10; j++){
          data[node][j] = getVal(buffer[16+j], buffer[17+j]);
        }
      }
    } catch(IOException e){
      print("Caught an IOException. Not sure what to do.");
    }
  }
}

/**
   Combine two bytes to create an unsigned short.
*/
int getVal(byte val1, byte val2){
  int val = 0;
  val += (val1 & 0x000000FF) << 8;
  val += (val2 & 0x000000FF);
  return val;
}

/**
   Connect to the server.
*/
void connect(String host, int port){
  try{
    socket = new Socket(this.host, this.port);
    input = socket.getInputStream();
    output = socket.getOutputStream();
    // Connect, read two bytes.
    while(input.available() < 2); // Block until 2 bytes available.
    input.read();
    input.read();
    // Send "U ".
    output.write("U ".getBytes());
    ControllerInterface[] controllers = controlP5.getControllerList();
    for(ControllerInterface c : controllers){ // Clean up the interface.
      controlP5.remove(c.name());
    }
    generateInterface();
  }
  catch(Exception e){
    controlP5.addTextlabel("errorField", "Sorry, connection could not be made.",
                           100, 100);
  }
}