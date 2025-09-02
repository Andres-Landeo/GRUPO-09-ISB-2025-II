# <ins>EMG Physical Action DataSet</ins>

## Relevant information:   
#### Protocol:
Three male and one female subjects (age 25 to 30), who have experienced aggression in scenarios such as physical fighting, took part in the experiment. Throughout 20 individual experiments, each subject had to perform ten normal and ten aggressive activities. Regarding the rights of the  subjects involved, ethical regulations and safety precaution have been followed based on the code of ethics of the British psychological society. The regulations explain the ethical legislations to be applied when experiments with human subjects are conducted. According to the experimental setup and the precautions taken, the ultimate risk of injuries was minimal. The subjects were aware that since their involvement in this series of experiments was voluntary, it was made clear that they could withdraw at any time from the study.

#### Instrumentation:
The Essex robotic arena was the main experimental hall where the data collection took place.
With area 4x5.5m, the subjects expressed aggressive physical activities at random locations. A professional kick-boxing standing bag has been used, 1.75m tall, with a human figure drawn on its body. The subjects performance has been recorded by the Delsys EMG apparatus, interfacing human activity with myoelectrical contractions. Based on this context, the data acquisition process involved eight skin-surface electrodes placed on the upper arms (biceps and triceps), and upper legs (thighs and hamstrings).

#### Data Setup:
The overall number of electrodes is 8, which corresponds to 8 input time series one for a muscle channel (ch1-8). Each time series contains ~10000 samples (~15 actions per experimental session for each subject).


### Number of Instances: ~10,000 

### Number of Attributes: 8

## Attribute Information:
   Each file in the dataset contains in overall 8 columns, and is organised as follows:

<table>
    <thead>
        <tr>
            <th>Segment</th>
            <th>Channel</th>
            <th>Muscle</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=2 align="center">R-Arm</td>
            <td align="center">Ch1</td>
            <td align="center">R-Bic</td>
        </tr>
        <tr>
            <td align="center">Ch2</td>
            <td align="center">R-Tri</td>
        </tr>
        <tr>
            <td rowspan=2 align="center">L-Arm</td>
            <td align="center">cC3</td>
            <td align="center">L-Bic</td>
        </tr>
        <tr>
            <td align="center">Ch4</td>
            <td align="center">L-Tri</td>
        </tr>
        <tr>
            <td rowspan=2 align="center">R-Leg</td>
            <td align="center">Ch5</td>
            <td align="center">R-Thi</td>
        </tr>
        <tr>
            <td align="center">Ch6</td>
            <td align="center">R-Ham</td>
        </tr>
        <tr>
            <td rowspan=2 align="center">L-Leg</td>
            <td align="center">Ch7</td>
            <td align="center"> L-Thi</td>
        </tr>
        <tr>
            <td align="center">Ch8</td>
            <td align="center">L-Ham</td>
        </tr>
    </tbody>
</table>


<ins>Segment</ins>: A segment defines a body segment or limb.
- Right arm (R-Arm)
- Left arm (L-Arm)
- Right leg (R-Leg)
- Left leg (L-Leg)

<ins>Channel</ins>: A channel corresponds to an electrode attached on a muscle.

<ins>Muscle</ins>:  A pair of muscles that corresponds to a segment.
- R-Bic: right bicep (C1)
- R-Tri: right tricep (C2)
- L-Bic: left bicep (C3)
- L-Tri: left tricep (C4)
- R-Thi: right thigh (C5)
- R-Ham: right hamstring (C6)
- L-Thi: left thigh (C7)
- L-Ham: left hamstring (C8)


### Number of Classes: 20
   The dataset consists of 10 normal, and 10 aggressive physical actions.

   <ins>Normal</ins>: Bowing, Clapping, Handshaking, Hugging, Jumping, Running, Seating, Standing, Walking, Waving.

   <ins>Aggressive</ins>: Elbowing, Frontkicking, Hamering, Headering, Kneeing, Pulling, Punching, Pushing, Sidekicking, Slapping


### Other:
   The log folder contains the formatted data files that can be loaded by the commercial Delsys software for visualisation.
   The txt folder contains the actual EMG data.   
   Note that the data collected from 2nd subject have not been filtered so the time series are noisy.