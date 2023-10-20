# GameOfBacteria
An educational simple game to show interaction between antbiotics and bacteria.
Certainly, here are the README files for your software in both English and Italian:

**SCROLL DOWN FOR ITALIAN**

# Bacteria vs. Antibiotics

![Game Screenshot](/img/screenshot.png)

## Disclaimer

This software is provided "as is," without any express or implied warranties of its operation.

The use of this software is at your own risk. The author assumes no responsibility for direct, indirect, incidental, or consequential damages resulting from the use, proper or improper, of this software.

By continuing to use this software, you agree to be bound by the terms of this disclaimer.

The source code of this software is distributed under the GPL-3.0 license, excluding audio effects and icons:
[GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html)

**Notes:**
- The audio effects used in this software come from free sources found on YouTube, without a license or under a Creative Commons license (creativecommons.org).
- The music is generated with Beatoven.ai and used with a valid worldwide license.
- Programmed in Python.

The purpose of the software is to entertain and, at best, provide a fun way to understand the behavior of bacteria and antibiotics.

The simulations in this game are quite realistic but are still influenced by random events (for entertainment purposes). They may not always represent real treatment situations or real situations in general.

It is the responsibility of the teacher, and an exercise for the student, to understand when the outcome of a game can be compared to real events to receive a stimulus to delve deeper.

The software developer does not assume responsibility for the accuracy of the medical information included.

The game can be a support for study but requires the presence and/or explanations of an expert teacher who can benefit from proposing simulations in the classroom.

Students approaching this game to gain knowledge must responsibly compare the medical information presented in the game with those from accredited or recognized sources.

## Game Rules

**1. Colored cells are bacteria. Green or purple if resistant to antibiotics:**

   - They replicate during the game and are killed by antibiotics.

**2. White cells are antibiotics. Administer them by pressing 'Antibiotic':**

   - You can treat the infection only when it starts causing symptoms.
   - Antibiotics are depleted and must be administered regularly.
   - The patient dies if they take too many antibiotics.
   - If antibiotics run out, bacteria become resistant.

**3. You can cause resistance by pressing 'Resistance':**

   - Bacteria require higher antibiotic doses.
   - They try not to be reached by antibiotics.
   - If a resistant bacterium dies, it deactivates an antibiotic molecule.
   - Deactivated antibiotics turn yellow and are destroyed.
   - If you administer antibiotics for too many consecutive days, you will develop resistance.
   - You have a 5% chance of curing a patient with resistance but also a chance to receive random bonuses.

**4. Even if the patient is not infected with a resistant bacterium, you can encounter three levels of difficulty:**

   - Easy: The person has a phenomenal immune system.
   - Routine: The immune system works, but don't underestimate anything.
   - Difficult: The person is immunosuppressed; the infection will be tough.

**5. Be mindful of time; these circumstances can make you lose points:**

   - If treatment lasts too long, the patient may become depressed.
   - The person may worsen and die with prolonged treatment.
   - Fatigue could lead to errors in therapy.

You must decide when to start treatment and how frequently to continue it.

**Caution: Resistance requires more antibiotics, but you might kill the patient!**
![Game Screenshot](game_screenshot.png)

Bacteria will pass resistance through their plasmids.
If resistance develops, you must have enough points to sustain the final challenge, which will be ONLY against resistant bacteria.

A tip: your medical supervisor is breathing down your neck, waiting for your next mistake!

## Scoring

**You receive points for:**

   - Duration of the patient's life without symptoms.
   - Killing resistant and non-resistant bacteria.
   - Curing the disease.

**Points are deducted for:**

   - Endangering the patient.
       - Causing resistance.
       - Risk of sepsis.
       - Overusing antibiotics.
       - Taking too long to cure the person.
       - Administering the wrong therapy: this happens if the treatment is too long (red cells).
   - Patient's death.
   - Antibiotic administration.
   - Each duplication of a resistant or non-resistant bacterium.
   - If you are fired by the medical supervisor.

**Keyboard Shortcuts:**

   - ENTER: Administer a dose of antibiotic.
   - SPACE: Develop resistance.
   - ESC: Restart the game.

Good luck in your fight against infection!

---

**README (Italian)**

# Batteri contro Antibiotici

![Game Screenshot](img/screenshot.png)

## Disclaimer

Questo software è fornito 'così com'è', senza alcuna garanzia, esplicita o implicita, sul suo funzionamento.

L'uso di questo software è a proprio rischio e pericolo. L'autore non si assume alcuna responsabilità per danni diretti, indiretti, accidentali o consequenziali derivanti dall'uso, proprio o improprio, di questo software.

Continuando a utilizzare questo software, l'utente accetta di essere vincolato dai termini di questo disclaimer.

Il codice sorgente di questo software è distribuito sotto la licenza GPL-3.0, non sono inclusi gli effetti audio e le icone:
[GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html)

**Note:**
- Gli effetti audio utilizzati in questo software provengono da fonti gratuite reperite su YouTube, senza licenza o sotto licenza Creative Commons (creativecommons.org).
- La musica è generata con Beatoven.ai ed usata con regolare licenza valida in tutto il mondo.
- Programmato in linguaggio Python.

Lo scopo del software è divertire, al massimo fare comprendere in modo divertente il comportamento di batteri e antibiotici.

Le simulazioni in questo gioco sono piuttosto realistiche, ma restano comunque influenzate da eventi casuali (anche per scopo di intrattenimento), e potrebbero non rappresentare sempre situazioni reali di cura, o reali in generale.

È responsabilità del docente, ed un esercizio per lo studente, comprendere quando il risultato di una partita possa essere confrontato con eventi reali, al fine di ricevere uno stimolo ad approfondirli.

Lo sviluppatore del software non si assume la responsabilità per l'accuratezza delle informazioni mediche incluse.

Il gioco può essere un supporto per lo studio, ma necessita della presenza e/o delle spiegazioni di un docente esperto, che può trarne vantaggio per proporre delle simulazioni in aula.

Lo studente che si approccia a questo gioco per ricevere delle nozioni, deve responsabilmente confrontare le informazioni mediche presentate nel gioco con quelle di fonti accreditate o riconosciute.

## Regole del gioco
