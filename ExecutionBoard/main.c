/**
  Generated Main Source File

  Company:
    Microchip Technology Inc.

  File Name:
    main.c

  Summary:
    This is the main file generated using PIC10 / PIC12 / PIC16 / PIC18 MCUs

  Description:
    This header file provides implementations for driver APIs for all modules selected in the GUI.
    Generation Information :
        Product Revision  :  PIC10 / PIC12 / PIC16 / PIC18 MCUs - 1.81.6
        Device            :  PIC18F26K83
        Driver Version    :  2.00
*/

/*
    (c) 2018 Microchip Technology Inc. and its subsidiaries. 
    
    Subject to your compliance with these terms, you may use Microchip software and any 
    derivatives exclusively with Microchip products. It is your responsibility to comply with third party 
    license terms applicable to your use of third party software (including open source software) that 
    may accompany Microchip software.
    
    THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER 
    EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY 
    IMPLIED WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS 
    FOR A PARTICULAR PURPOSE.
    
    IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE, 
    INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND 
    WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP 
    HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO 
    THE FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL 
    CLAIMS IN ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT 
    OF FEES, IF ANY, THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS 
    SOFTWARE.
*/

#include "mcc_generated_files/mcc.h"
#include "mcc_generated_files/i2c1_master.h"
#include "mcc_generated_files/uart1.h"


int flag = 0;

char uart_datum = 'F';

void delay (int timeout){
    
    for (volatile int i = 0; i < timeout; ++i){}
    
    
}



void handlerFunc(void){
    flag = 4;
    
    IO_RA4_Toggle(); 
  
    
    //while (!UART1_is_rx_ready());

    //uart_datum = UART1_Read();
    UART1_Receive_ISR();
    return;
     
}


void main(void)
{
    // Initialize the device
    SYSTEM_Initialize();
    
    PIN_MANAGER_Initialize();
    
    // Initialize I2C bus
    I2C1_Initialize();
    UART1_Initialize();

    // var to store address of sensor 
    i2c1_address_t myAddr = 0x80;
    
    // placeholder var for return 
    i2c1_error_t error = I2C1_BUSY;
    
    //buffer for I2C transactions
    char i2c_dataBuff[5];
    I2C1_SetBuffer((void *)i2c_dataBuff, 5);
    
    //data for test UART stuff
    uint8_t uartdatum = 'D';
    
    UART1_SetRxInterruptHandler(&handlerFunc);
    
    
    
    // If using interrupts in PIC18 High/Low Priority Mode you need to enable the Global High and Low Interrupts
    // If using interrupts in PIC Mid-Range Compatibility Mode you need to enable the Global Interrupts
    // Use the following macros to:

    
    
    
    // Enable the Global Interrupts
    INTERRUPT_GlobalInterruptEnable();

    // Disable the Global Interrupts
    //INTERRUPT_GlobalInterruptDisable();

    while (1)
    {
       //  error =  I2C1_Open(myAddr);

        IO_RA5_Toggle(); 
        
        
        delay(4000);
        delay(4000);
        
        // send UART thing
       //  UART1_Write(uartdatum);
         
       //  while (!UART1_is_tx_done());
      
        // error = I2C1_MasterOperation(true); // read from I2C buff
    }
}
/**
 End of File
*/