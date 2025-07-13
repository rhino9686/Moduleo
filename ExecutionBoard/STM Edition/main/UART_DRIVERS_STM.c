#include "main.h"
 
uint8_t UART1_rxBuffer[4] = {0};
 
UART_HandleTypeDef huart1;
DMA_HandleTypeDef hdma_usart1_rx;
 
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_USART1_UART_Init(void);

int index;

void handleUARTBuffer();
 
int main(void)
{
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_DMA_Init();
    MX_USART1_UART_Init();
 
    HAL_UART_Receive_DMA (&huart1, UART1_rxBuffer, 4);
 
    index = 0;

    while (1)
    {
        handleUARTBuffer();
    }
 
}
 
void handleUARTBuffer(){

    int magnitudeRelevant = 0;
    int fetchingData = 0;

    char cmdByte = (char)UART1_rxBuffer[0];
    char magByte = (char)UART1_rxBuffer[1];
    char dataByte = (char)UART1_rxBuffer[2];
    char termByte = (char)UART1_rxBuffer[3];

    //make sure termination Byte is Z
    if (termByte != 'Z'){
        //Maybe shut off all PWMs as a safety measure?
        return;
    }

    //interpret command Byte
    switch (cmdByte) {

        //Going forward constantly
        case 'f':
            { //printf("going forward");
            break;
            }
        //Going backwards constantly
        case 'b':
           { //printf("going backwards");
            break;
            }
        //turning right constantly
        case 'r':
            { //printf("turning right constantly");
            break;
            }
        //turning left constantly
        case 'l':
            { //printf("turning left constantly");
            break;
            }

         //halting immediately
        case 'h':
            { //printf("halting immediately");
            break;
            }

        //adjusting speed
        case 's':
            { //printf("adjusting speed");
            
            break;
            }

        //requesting data
        case 'd':
            { //printf("Case 3 is Matched.");
            fetchingData = 1;
            break;
            }

 
        default:
            { //printf("Default case is Matched.");
            break;
            }
    }


    if (magnitudeRelevant){
        //hold timer for amount of seconds in magbyte
        //then halt
        //adjusting speed will not use this block 
    } 
    if (fetchingData){
        //use databyte to see what they need, then do that
    }

    return;

}


//We should only receive 4 bytes at a time
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    HAL_UART_Transmit(&huart1, UART1_rxBuffer, 4, 100);
    HAL_UART_Receive_DMA(&huart1, UART1_rxBuffer, 4);
}