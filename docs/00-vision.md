# Vision

## The problem
Getting a basic health check usually means appointments, queues, separate visits for
separate tests, and days of waiting for results. In many places there are simply not
enough doctors. People delay care until a problem becomes serious.

## Long-term goal
A pod where a person lies down and, within minutes, safe sensors and AI give a clear
picture of what may be wrong — inspired by the medical bay in the film *Elysium*.

## What v0.1 is
A **triage station**: it measures vital signs and simple body signals using only existing,
safe, non-invasive technology, and says *"this looks normal"* or *"this looks abnormal —
see a doctor (today / soon)"*. It does **not** give a diagnosis.

### In scope (v0.1)
- Patient platform (bed or reclined chair) with sensor mounts
- Camera: heart rate (rPPG), breathing rate, facial expression
- Thermal camera: skin temperature, fever
- ECG (single or 3-lead)
- Pulse oximetry (SpO2)
- Blood pressure (automatic cuff)
- Microphone: cough and breathing sounds
- AI that combines all readings into a triage result with a confidence level

### Out of scope (v0.1) — later versions
- Anything that uses ionising radiation (X-ray, CT)
- MRI
- Blood sampling (planned for a later version: finger-prick analyser)
- Ultrasound (planned for a later version: handheld probe, then robotic arm)
- Treatment of any kind

## Success criteria (v0.1)
- Measures all vital signs above in under 5 minutes
- Each reading checked against a reference device (e.g. a medical-grade pulse oximeter)
- Triage output explains which readings triggered it
- Full design, code and study record published so others can build on it
