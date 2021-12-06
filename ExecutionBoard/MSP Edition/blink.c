#include <msp430.h>				
#include <stdint.h>
#include <stdbool.h>

/**
 * blink.c
 */

//******************************************************************************
// Pin Config ******************************************************************
//******************************************************************************

#define LED_OUT     P1OUT
#define LED_DIR     P1DIR
#define LED0_PIN    BIT0
#define LED1_PIN    BIT1

#define SLAVE_ADDR  0x48



//******************************************************************************
// Device Initialization *******************************************************
//******************************************************************************
void initClockTo16MHz()
{
    if (CALBC1_16MHZ==0xFF)             // If calibration constant erased
    {
        while(1);                       // do not load, trap CPU!!
    }
    DCOCTL = 0;                         // Select lowest DCOx and MODx settings
    BCSCTL1 = CALBC1_16MHZ;             // Set DCO to 16MHz
    DCOCTL = CALDCO_16MHZ;
}


void initGPIO()
{
    //LEDs
    LED_OUT &= ~(LED0_PIN | LED1_PIN);  // P1 setup for LED & reset output
    LED_DIR |= (LED0_PIN | LED1_PIN);

    //I2C Pins
    P3SEL |= BIT1 | BIT2;                     // P3.1,2 option select
}


void initI2C()
{
    UCB0CTL1 |= UCSWRST;                      // Enable SW reset
    UCB0CTL0 = UCMST + UCMODE_3 + UCSYNC;     // I2C Master, synchronous mode
    UCB0CTL1 = UCSSEL_2 + UCSWRST;            // Use SMCLK, keep SW reset
    UCB0BR0 = 160;                            // fSCL = SMCLK/160 = ~100kHz
    UCB0BR1 = 0;
    UCB0I2CSA = SLAVE_ADDR;                   // Slave Address
    UCB0CTL1 &= ~UCSWRST;                     // Clear SW reset, resume operation
    UCB0I2CIE |= UCNACKIE;
}



void main(void)
{






	WDTCTL = WDTPW | WDTHOLD;		// stop watchdog timer
	P1DIR |= 0x01;					// configure P1.0 as output

	volatile unsigned int i;		// volatile to prevent optimization

	while(1)
	{
		P1OUT ^= 0x01;				// toggle P1.0
		for(i=10000; i>0; i--);     // delay
	}
}
