# Learning log

## 00-setup
Just a series of tests to explore the sounddevice package used in this repo and setting up the env for testing. 

## 01-Chirp Capture & Matched Filter
Recorded a 5 pulse, linearly modulated chirp from my speaker at a folded table held perpendicular to the speaker at 1 meter and 1.5 meter distances respectively. Speakers were at max volume with an amplitude of .5. The room recorded in was a small home office space with all objects removed between and to the sides of the speaker and the walls. 

Using signal compression I was able to consistently identify the echo of the table in the data with 10cm of the actual recorded distance. Interestingly, all of my results were short by almost exactly 10cm indicating that this may simply be an artifact of my getto calibration. Regardless, the main point is seeing the power of match filtering first hand. The echos are extremely difficult to identify in the raw data, but became very apparent after the filter pass. Seeing this in action on a physical demonstration was cool. 

## 02-Using Doppler to measure velocity
Ran a demo on both synthetic data and real radar recordings of a reflective target floating on waves. In short, doppler filtering works by looking at the recorded signal across multiple pulses and examining how the phase of that signal changes across all of those pulses. A target moving towards the sensor will increase the freqency of the recorded echo and by measuring this shift we can pull out the velocity of the object. Stationary objects just return a constant echo which we can also use to filter them out as just ground clutter. 

The real data used as part of this experiment was of a stationary radar pointed at a reflective and anchored target on the sea. The velocity of this target was really low since it moved with the waves. It's a little hard to spot because of the clutter the waves produce since they are not perfectly still, but we were still able to detect it within that clutter and match the rage exactly. 