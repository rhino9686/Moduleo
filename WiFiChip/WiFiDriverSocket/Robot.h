

//Character definition constants
#define FORWARD 'F'       //  To send message over UART for drone to go forward for a unit of time
#define FORWARD_CONT 'f'  //  To send message over UART for drone to continuously move forward
#define BACKWARD 'B'      //  To send message over UART for drone to go backward for a unit of time
#define BACKWARD_CONT 'b' //  To send message over UART for drone to continuously move backwards
#define LEFT 'L'          //  To send message over UART for drone to rotate left for a unit of time
#define RIGHT 'R'         //  To send message over UART for drone to rotate right for a unit of time
#define HALT 'H'          //  To send message over UART for drone to halt

class RobotTank{

  public:
      int speed = 0;
      char direction = 'F';
};