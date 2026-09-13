#include "PlutoPilot.h"
#include "Print.h"
#include "Control.h"
#include "Sensor.h"

#define IR_SENSOR_PORT 0  // D0

void plutoInit();
void onLoopStart();
void plutoPilot();
void onLoopFinish();

void plutoInit()
{
    Print_P("Pluto Init Done");
}

void onLoopStart()
{
    // Optional
}

void plutoPilot()
{
    int irValue = getDigitalSensor(IR_SENSOR_PORT);  // returns 0 or 1

    if (irValue == 0)  // Obstacle detected
    {
        setPitch(0);
        setRoll(0);
        setYaw(0);
        setThrottle(1500);
        Print_P("Obstacle Detected - Hovering");
    }
    else
    {
        setPitch(300);
        setRoll(0);
        setYaw(0);
        setThrottle(1500);
        Print_P("Path Clear - Moving Forward");
    }
}

void onLoopFinish()
{
    // Optional
}