#!/usr/bin/env python3
"""ATLAS English Academy v2.0: reproducible original studio curriculum/visual-art compiler.

The dataset uses newly authored scenarios, practice texts and deterministic assessment
rules, not scraped book content or downloaded grade-bank materials. Run from any cwd.
"""
from __future__ import annotations
import csv, html, json, math, re
from pathlib import Path
from hashlib import sha256

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'source'
DATA = SRC / 'studio-data'
ART = SRC / 'illustrations'
LEVELS = [('PK','Preschool','Emergent literacy'),('K','Kindergarten','Early literacy')] + [(str(i),f'Grade {i}','Elementary' if i<6 else 'Middle School' if i<9 else 'High School') for i in range(1,13)] + [('C1','College I','College'),('C2','College II','Advanced college')]
STRANDS = [
 ('phonics','Sounds, Phonics & Word Study','Sound scientist','letter-sound patterns, syllables and morphology'),
 ('fluency','Fluency & Reading Strategies','Fluency coach','phrasing, punctuation and purposeful rereading'),
 ('vocabulary','Vocabulary & Word Origins','Word detective','context clues, precision and word relationships'),
 ('grammar','Grammar & Sentence Craft','Sentence engineer','clear sentences, punctuation and editing'),
 ('fiction','Fiction & Narrative','Story explorer','plot, character, setting and theme'),
 ('poetry','Poetry & Drama','Poetry performer','imagery, sound and interpretation'),
 ('information','Nonfiction & Media Literacy','Information explorer','main ideas, structure and verification'),
 ('evidence','Inference & Textual Evidence','Evidence analyst','observation, inference and strong support'),
 ('composition','Composition & Revision','Author’s studio','drafting, organizing and improving writing'),
 ('rhetoric','Argument & Rhetoric','Argument architect','claims, warrants, audiences and counterarguments'),
 ('research','Research & Citation','Research librarian','questions, source quality and attribution'),
 ('speaking','Speaking & Listening','Conversation leader','listening, discussion and presentation'),
]

# Each record represents an intentionally distinct fictional or instructional mini-case:
# title | actor | setting | initial action | observed concrete evidence | response | outcome | interpretive limitation | vocabulary anchor
RAW = {
'phonics': [
 'The Bell and the Boat|Nia|a riverside classroom|sorted picture cards|bell and boat both begin with /b/|tapped the starting sound twice|her classmates named a matching pair|letters sometimes represent different sounds|alliteration',
 'The Syllable Train|Omar|a reading corner|clapped the name banana|his hands moved three times|marked the beats with three counters|the class divided the word into syllables|spoken syllables do not always match spelling chunks|syllable',
 'The Silent Letter|Rae|a school garden|compared knee and nest|knee begins with a silent k|highlighted the initial letter cluster|the class noticed that spelling and sound can differ|one spelling example cannot explain every silent letter|phoneme',
 'The Word Family Wall|Leo|a bright hallway|paired light with night|both words shared the written ending ight|built a rhyming word wall|his group checked each new example aloud|some similar endings do not rhyme|rime',
 'The Prefix Puzzle|Mina|the school library|unwrapped a paper labeled replay|re- can signal doing something again|split the word into prefix and base|her group predicted the meaning before reading|prefix meanings depend on context|morpheme',
 'The Roots Workshop|Sol|a science club|compared telescope and microscope|scope relates to looking or viewing|drew a word-root family tree|students connected technical words through structure|shared roots do not make words interchangeable|etymology',
 'The Long Vowel Trail|Ivy|a phonics lab|read cap and cape|the final e changed the vowel sound|moved letter tiles to form new pairs|a small spelling change altered pronunciation|the pattern has exceptions|vowel',
 'The Sound Map|Tariq|a theater rehearsal|tracked the sounds in ship|sh represented one sound|marked three sounds on a small chart|the cast pronounced the word consistently|letter count is not necessarily sound count|digraph',
],
'fluency': [
 'The Pause at the Comma|Mia|the school auditorium|read a speech too quickly|the comma divided two meaningful phrases|marked pauses in the margin|listeners understood the second reading|pausing is not the same as understanding a claim|prosody',
 'The Repeated Reading|Eli|the reading room|reread a difficult paragraph|his second reading included fewer hesitations|practiced a phrase three times|the sentence sounded smoother|speed alone does not measure comprehension|fluency',
 'The Question Voice|Ada|a puppet show|read a question like a statement|the question mark signaled a change in tone|tested two different intonations|the audience recognized the question|not all questions require rising pitch|intonation',
 'The Dialogue Switch|Noel|the class stage|read two characters without changing voice|quotation marks identified separate speakers|marked each speaker in two colors|the exchange became easier to follow|expressive performance should not distort text|dialogue',
 'The Poetry Beat|Kai|a poetry club|chanted a poem in one flat tone|line breaks created opportunities for pacing|rehearsed varying pauses and emphasis|the poem gained expressive contrast|line endings do not always signal full stops|rhythm',
 'The Newsroom Read|Zoe|a school podcast|prepared to read a brief report|names and numbers required careful articulation|practiced unfamiliar terms before recording|the recording became clearer|confident delivery does not prove factual accuracy|articulation',
 'The Meaningful Phrase|Pax|a literacy workshop|divided a long sentence into phrases|each phrase contained a connected idea|marked grammatical boundaries with pencil slashes|reading sounded more natural|phrasing must preserve the original meaning|syntax',
 'The Evidence Read-Aloud|Uma|a public forum rehearsal|emphasized a dramatic adjective|the paragraph’s crucial evidence was a number|rehearsed emphasizing the documented figure|listeners noticed the evidence instead of the drama|emphasis can bias interpretation|emphasis',
],
'vocabulary': [
 'The Glimmering Lantern|Lena|a museum story corner|encountered the word glimmer|a dim lantern gave off a small light|compared glimmer with shine and blaze|she chose a word that fit the scene|near-synonyms differ in intensity|nuance',
 'The Careful Forecast|Arun|a weather club|read the word probable|the report said rain was likely but not certain|placed probability words on a scale|the group used more calibrated language|likely does not mean guaranteed|connotation',
 'The Context Detective|Sara|a library mystery game|encountered the word reluctant|a character hesitated before agreeing|underlined the surrounding clues|her team inferred unwillingness|a clue can suggest but not prove a definition|context',
 'The Opposite Shelf|Jude|a classroom bookstore|sorted scarce and abundant|one shelf held two books and another held many|made a contrast chart|his partners distinguished the terms|opposites can depend on a comparison|antonym',
 'The Tone Translator|Leah|a debate club|compared stubborn and determined|both words suggested persistence|rewrote a sentence for different audiences|the sentence changed its emotional force|word choice can frame a reader’s judgment|diction',
 'The Roots of Transport|Mateo|a transit museum|noticed transport and portable|both words carried the port root|sketched a network of related words|the team inferred a shared idea of carrying|not all look-alike words share a history|root',
 'The Multiple-Meaning Key|Fern|an engineering lab|read the word current|the text mentioned both electricity and a river|identified the subject of each sentence|she selected the correct sense in context|dictionaries list senses that are not equally relevant|polysemy',
 'The Precise Verb|Imani|a writing workshop|revised the phrase went quickly|the character sprinted across the courtyard|replaced a vague verb with sprinted|the revision made motion easier to picture|vivid language should still be accurate|precision',
],
'grammar': [
 'The Comma Clinic|Evan|the editing desk|edited a two-part sentence|two independent clauses had only a comma between them|added a conjunction after the comma|the sentence no longer had a comma splice|other correct punctuation choices also exist|clause',
 'The Verb Agreement Lab|Ava|the language studio|revised a sentence about several birds|the plural subject required a plural verb|changed flies to fly|the subject and verb agreed|phrases between subject and verb can mislead|agreement',
 'The Pronoun Puzzle|Bo|the community newsletter|found an unclear pronoun|two people appeared before the word she|replaced the pronoun with the intended name|the reader could identify the person|pronouns require context to be clear|antecedent',
 'The Modifier Mystery|Rina|a newspaper club|read a misplaced modifier|the sentence appeared to describe a walking backpack|moved the descriptive phrase beside the student|the sentence described the intended action|more than one revision may be grammatical|modifier',
 'The Parallel Path|Theo|a college-prep seminar|edited a three-part list|two items were verbs and one was a noun|rewrote all items with matching forms|the list became easier to compare|parallel form does not replace logical accuracy|parallelism',
 'The Apostrophe Workshop|Maya|a school bakery|wrote a sign for two bakers|the cakes belonged to both bakers|placed the apostrophe after the plural s|the possessive relationship became clear|plural and possessive forms differ|possessive',
 'The Active Voice Choice|Gabe|a local history club|compared active and passive versions|one sentence emphasized the actor and the other the event|selected a voice that fit the purpose|the paragraph gained a clearer focus|passive voice is not always incorrect|voice',
 'The Sentence Boundary|Nora|a language-learning center|joined two independent sentences without punctuation|the reader had no clear boundary|separated the statements with a period|the ideas became easier to follow|a semicolon may also work in context|run-on',
],
'fiction': [
 'The Lost Map|Niko|a coastal village|found a map beside the old pier|one corner showed a path drawn in blue|asked an elder about the drawing|he learned the path led to a public garden|the map did not identify who drew it|setting',
 'The Paper Bridge|Tess|a classroom makerspace|promised to build a bridge from paper|the first bridge folded under one book|added triangular supports and retested it|the second design held two books|one test does not demonstrate every condition|conflict',
 'The Midnight Library|Wren|a quiet town library|heard a soft tapping after closing|a branch touched the window in the wind|followed the sound instead of panicking|the mystery had an ordinary explanation|not every unexplained sound has the same cause|suspense',
 'The Borrowed Compass|Hugo|a mountain camp|borrowed a compass from a friend|the needle pointed north despite his guessed route|stopped and rechecked the trail markers|the group reached the correct path|a compass alone cannot describe terrain hazards|character',
 'The Lantern Keeper|Jia|a lakeside harbor|saw the signal light flicker|a loose cable interrupted the lantern|reported the problem and carried a backup|travelers could still see a safe signal|the story does not establish who damaged the cable|theme',
 'The Quiet Inventor|Milo|a crowded invention fair|made a device to collect rainwater|a small mesh screen kept leaves out|explained the design with a simple diagram|visitors understood his idea despite his shy voice|interest from visitors is not evidence of reliability|motivation',
 'The Garden Gate|Sofia|a community garden|found the gate open one morning|a strong wind had bent the loose latch|worked with neighbors to repair it|the vegetables remained protected|an open gate alone does not identify wrongdoing|inference',
 'The Two Invitations|Eden|a bustling school|received invitations to two events|both gatherings happened at the same time|spoke honestly with each group|the friends planned a shared event later|a compromise cannot satisfy every preference|resolution',
],
'poetry': [
 'Rain on the Window|Elia|a rainy classroom|wrote about drops on glass|the tapping sounded like tiny footsteps|used a simile in the second line|the class heard the rhythm of the rain|a simile suggests rather than reports literal fact|simile',
 'The Blue Hour|Samir|a quiet rooftop|described the sky after sunset|the last gold light faded into blue|used a color image to signal transition|the poem suggested calm without naming it|readers may interpret the mood differently|imagery',
 'The Dancing Leaves|Mira|a garden path|watched leaves twist in wind|the leaves seemed to dance together|gave the leaves a human action|the lines felt playful|personification does not make leaves conscious|personification',
 'The Clock’s Voice|Rory|a historic station|heard a clock tick in the hall|its sound repeated at even intervals|used repeated consonants in a line|the rhythm suggested passing time|sound patterns do not dictate a single theme|alliteration',
 'The River Mirror|Anya|a riverside trail|noticed clouds reflected on water|the surface changed when a boat passed|called the river a moving mirror|the metaphor connected motion and reflection|metaphors need not be taken literally|metaphor',
 'The Empty Chair|Bryn|an evening theater|saw a chair under a single light|the space remained empty during rehearsal|wrote two possible readings of the image|the audience considered absence and expectation|the symbol can carry several meanings|symbol',
 'The Four-Line Scene|Iris|a poetry workshop|drafted a short four-line poem|the first and third lines ended with similar sounds|tested the pattern aloud|the class described an alternating sound pattern|not all poetry uses end rhyme|rhyme',
 'The Stage Direction|Noa|a small school theater|read a script with stage directions|one character moved away before replying|performed the gesture before the dialogue|the conflict became visible without narration|a stage direction is not a character’s spoken line|subtext',
],
'information': [
 'The Neighborhood Garden|Cora|a community meeting|examined a proposed garden plan|the map showed six raised beds and a rain barrel|summarized the main goal and details|the group compared available space with its needs|a proposed plan does not prove future success|main idea',
 'The Bus Route Chart|Malik|a transit workshop|studied a fictional schedule|Route A arrived every 20 minutes and Route B every 30|made a comparison table|the group found the more frequent route|frequency does not establish reliability|compare',
 'The Food Waste Study|Talia|a school cafeteria|tracked leftover lunches for one week|Monday had twelve leftovers and Friday had seven|created a bar chart|the class noticed a decrease across the sample|a short sample does not establish a trend for the year|data',
 'The River Diagram|Quinn|an ecology club|drew a stream’s route through a valley|water moved from higher ground toward a basin|labeled each part of the diagram|students could follow the system|a simple diagram leaves out many processes|diagram',
 'The Device Repair Guide|Zara|a makerspace|read a fictional repair checklist|the first step said to disconnect power|put the safety step before inspection|the team followed an orderly sequence|a checklist cannot cover every safety hazard|procedure',
 'The Library Survey|Ben|a town library|reviewed a sample patron survey|18 people preferred evening hours and 11 preferred mornings|reported both totals before drawing a conclusion|the committee discussed an evening pilot|the survey sample may not represent everyone|sample',
 'The Water Bottle Label|Dina|a consumer literacy class|compared two product labels|one reported 500 mL and the other 750 mL|distinguished volume from advertising adjectives|students avoided a misleading comparison|larger volume does not automatically mean higher quality|quantify',
 'The Habitat Poster|Emil|a biology classroom|studied a fictional wetland poster|its diagram showed reeds, insects and frogs|identified an interaction among organisms|the class drew a simple food connection|a poster is not a complete ecological model|relationship',
],
'evidence': [
 'The Mysterious Footprints|Luz|a school courtyard|found shoe prints near a watering can|the soil was wet and the prints pointed toward the gate|photographed the patterns before concluding|she reported what she could directly see|prints alone do not identify who made them|observation',
 'The Missing Paintbrush|Ari|an art classroom|noticed a brush missing from a jar|a receipt showed supplies were moved to storage|checked the storage shelf|the brush was found in a labeled box|a missing item does not prove theft|corroboration',
 'The Library Traffic Claim|Nina|a neighborhood library|heard that attendance had doubled|a chart showed 40 visits one week and 55 the next|calculated the increase instead of repeating the claim|she revised the statement to match the data|two weeks do not establish a lasting pattern|claim',
 'The Noisy Hallway|Owen|a school hallway|reported an unusual sound after class|the recorder captured a rolling cart and conversation|compared the recording with witness descriptions|the group separated direct evidence from guesses|recordings can lack important context|inference',
 'The Bicycle Trace|Leila|a campus courtyard|saw a fresh tire mark near the bike rack|the tread had a repeating zigzag pattern|described the mark without naming a rider|the report distinguished trace and hypothesis|common tread patterns rarely identify a unique bicycle|uncertainty',
 'The Schedule Dispute|Marco|a student committee|heard two accounts of a meeting time|the published notice said 3:30 and a text message said 4:00|checked when each notice was created|the committee issued a corrected schedule|later evidence can supersede earlier notices|chronology',
 'The Broken Link|Esme|a digital research class|found an unattributed quotation online|the webpage omitted its author and source|searched for an original publication|the quotation remained unverified|repetition across websites does not prove authenticity|verification',
 'The Experiment Notebook|Jay|a science seminar|reviewed a class plant trial|one plant received sunlight and another was kept in shade|listed other uncontrolled variables|the group qualified its conclusion|different watering could also affect growth|control',
],
'composition': [
 'The Thank-You Note|Anika|a school office|drafted a thank-you message|her first version did not explain what help mattered|added a specific example from the event|the recipient could see the reason for thanks|the note should not exaggerate the assistance|audience',
 'The Clear Instructions|Perry|a robotics club|wrote directions for a paper model|the steps omitted the order of folding and cutting|numbered each action and tested it|a teammate followed the revised directions|different materials may require adjustment|sequence',
 'The Strong Topic Sentence|Ruth|a reading workshop|wrote a paragraph about libraries|the draft listed benefits without a central claim|added a topic sentence about community access|the details connected to one idea|a topic sentence must match its evidence|unity',
 'The Revision Conference|Luis|a writing center|shared a first draft about a parade|a reader could not tell when the events occurred|inserted time signals and checked chronology|the story became easier to follow|readers may still ask for more context|revision',
 'The Source Integration|Dahlia|a college seminar|added a quotation to a paper|the quotation appeared without an explanation|introduced the quotation and explained its relevance|the paragraph linked evidence to a claim|a quotation cannot substitute for reasoning|integration',
 'The Concise Email|Caleb|an internship office|drafted an email requesting information|the request was buried beneath unrelated details|moved the request into the first paragraph|the reader could identify the needed action|brevity must not omit essential context|conciseness',
 'The Reflective Journal|Sena|a creative-writing class|wrote about a difficult presentation|the first draft stated only that it felt hard|described one obstacle and one improvement|the reflection showed a learning process|one experience does not establish a permanent trait|reflection',
 'The Balanced Review|Felix|a film discussion club|wrote a review with only praise|one scene had unclear sound during dialogue|added a fair limitation and a specific example|the review offered a more balanced judgment|different viewers may value aspects differently|evaluation',
],
'rhetoric': [
 'The Park Bench Debate|Aisha|a city youth council|proposed adding two park benches|an accessibility walk found a long path without seating|connected the observation to the request|the council planned to examine locations|one walk does not measure every visitor’s needs|warrant',
 'The School Lunch Proposal|Drew|a student forum|asked for a second lunch line|students described waits longer than ten minutes|suggested a short timed trial|the group agreed to collect better data|testimony alone does not predict system costs|proposal',
 'The Persuasive Poster|Yara|a design class|made a poster about recycling|the first poster relied on an alarming slogan|replaced the slogan with a clear action and reason|viewers understood what they could do|clarity does not guarantee behavior change|purpose',
 'The Competing Priorities|Ezekiel|a school budget workshop|compared two student proposals|one improved library hours and another repaired sports equipment|listed benefits and trade-offs fairly|the team built a decision matrix|different audiences can weight priorities differently|counterargument',
 'The Opinion Column|Kemi|a student newspaper|wrote that all students preferred online books|her survey had responses from eight classmates|revised the claim to reflect the sample|the argument became more defensible|a small convenience sample is not representative|qualifier',
 'The Community Appeal|Ira|a neighborhood meeting|asked volunteers to plant shade trees|one street lacked shade near a playground|combined a concrete example with a feasible action|several neighbors asked for a site survey|a moving story does not replace feasibility analysis|appeal',
 'The Price Comparison|Vera|a consumer awareness club|argued that one package was cheaper|two packages had different quantities|computed price per unit|her classmates compared equal units|a lower unit price may not fit every need|reasoning',
 'The Fair Counterpoint|Micah|a mock senate session|argued for an earlier school start|some classmates depended on morning transportation|acknowledged the concern and proposed alternatives|the debate considered a wider set of consequences|a counterargument is not automatically a refutation|rebuttal',
],
'research': [
 'The Author Check|Nadia|a library media center|found a blog about ancient ships|the page gave no author or references|looked for credentials and cited studies|she marked the blog as a starting point only|lack of citations limits verification|authority',
 'The Date Matters|Silas|a history research desk|compared two articles about a changing policy|one article was five years older|checked publication dates and current documents|the team prioritized the more relevant evidence|newer sources can still be wrong|currency',
 'The Citation Trail|Helena|a college library|read a claim quoted from another article|the second article pointed to a primary report|followed the reference back to its origin|she distinguished a primary source from summaries|a primary source may still contain methodological flaws|attribution',
 'The Search Query|Avery|a digital research lab|searched broadly for river pollution|the results mixed tourism and environmental reports|added focused terms and a date range|the search returned more relevant leads|search rankings do not establish credibility|query',
 'The Paraphrase Workshop|Dario|a writing seminar|rewrote a report in nearly identical wording|the draft preserved the source’s sentence structure|restated the idea independently and cited the source|the revised paragraph had clearer attribution|paraphrase requires more than swapping synonyms|paraphrase',
 'The Source Comparison|Juno|a public health classroom|compared two fictional survey summaries|one surveyed 30 volunteers and the other 300 randomly selected people|listed sampling differences before citing results|her argument stated its uncertainty|sample size alone cannot remove bias|methodology',
 'The Research Question|Mae|a capstone planning workshop|began with a question about all technology|the question was too broad to answer in one paper|narrowed it to reading habits in one class|the investigation gained a feasible scope|narrow questions may still face data limitations|scope',
 'The Bibliography Check|Leo|a university writing lab|reviewed a student reference list|two entries omitted publication years|checked the source records and repaired the entries|readers gained better retrieval information|a complete citation does not validate a claim|citation',
],
'speaking': [
 'The Listening Circle|Hana|a classroom circle|prepared to answer before a partner finished|the partner’s main point came at the end|paused and paraphrased what she heard|the partner confirmed being understood|paraphrase can miss nuance without clarification|active listening',
 'The Clarifying Question|Moss|a science club|heard a vague proposed experiment|the phrase test it had no stated measurement|asked what outcome would be recorded|the group agreed on an observable measure|a clarified question does not guarantee a good design|clarification',
 'The Group Presentation|Jules|an exhibition hall|gave a talk while facing the screen|audience members could not hear key numbers|turned toward the audience and enlarged a chart|the next explanation was more accessible|volume alone is not the same as clear reasoning|delivery',
 'The Respectful Disagreement|Amina|a student council|disagreed with a friend’s proposal|the friend worried about fairness in assignments|restated the concern before offering evidence|the discussion stayed focused on the idea|respect does not require agreement|civility',
 'The Interview Practice|Kian|a career classroom|answered an interview prompt without an example|the answer contained a vague personal claim|added a situation, action and result|the listener could assess the concrete example|one example does not establish a universal ability|specificity',
 'The Roundtable Summary|Alma|a small conference room|listened to three competing suggestions|participants prioritized cost, access and timing|summarized points of agreement and disagreement|the group selected a follow-up question|summaries may unintentionally omit minority views|synthesis',
 'The Evidence Slide|Ty|a research presentation|displayed a crowded table on one slide|the key difference was a three-person change|highlighted the comparison and explained uncertainty|the audience identified the main result|a clear slide does not guarantee valid evidence|visual literacy',
 'The Opening Statement|Rosa|a mock hearing|started a speech without identifying the issue|listeners lacked context for her recommendation|opened with an issue, claim and roadmap|the audience could follow the argument|a persuasive opening must still be supported|organization',
]
}
assert set(RAW)=={x[0] for x in STRANDS}
assert all(len(items)==8 for items in RAW.values())

# Original term definitions and unit-specific practical response checks.
TERM_DEFINITIONS = {
'alliteration':'Repetition of an initial consonant sound in nearby words.',
'syllable':'A spoken word beat organized around a vowel sound.',
'phoneme':'The smallest contrastive unit of sound in a language.',
'rime':'The vowel and following sounds in a spoken syllable.',
'morpheme':'The smallest language unit carrying meaning or grammatical function.',
'etymology':'The study of a word’s origins and historical development.',
'vowel':'A speech sound produced with a relatively open vocal tract.',
'digraph':'Two letters used together to represent one sound.',
'prosody':'The rhythm, stress, and intonation of spoken language.',
'fluency':'Reading with accuracy, useful pacing, and meaningful phrasing.',
'intonation':'Variation in pitch while speaking.',
'dialogue':'Written or spoken conversation between people or characters.',
'rhythm':'A recurring pattern of beats, timing, or stress.',
'articulation':'Clear production of the sounds of speech.',
'syntax':'The patterns and principles of arranging words into sentences.',
'emphasis':'Extra prominence given to a word or idea.',
'nuance':'A subtle distinction in meaning, force, or feeling.',
'connotation':'Emotional or cultural associations added to a word’s literal meaning.',
'context':'Surrounding words or circumstances that help establish meaning.',
'antonym':'A word whose meaning contrasts with another word.',
'diction':'A speaker’s or writer’s choice of words.',
'root':'A base element that carries core meaning in related words.',
'polysemy':'A single word having two or more related meanings.',
'precision':'Using wording that fits an intended meaning accurately.',
'clause':'A group of words containing a subject and a predicate.',
'agreement':'Grammatical correspondence such as subject–verb number.',
'antecedent':'The noun or noun phrase a pronoun refers back to.',
'modifier':'A word or phrase that adds descriptive information.',
'parallelism':'Use of matching grammatical patterns for related ideas.',
'possessive':'A form that indicates ownership, belonging, or association.',
'voice':'A grammatical way of relating participants to an action, as in active or passive.',
'run-on':'Incorrectly joining independent clauses without a proper boundary.',
'setting':'The place, time, and conditions in which a narrative unfolds.',
'conflict':'An opposition, problem, or competing goal in a story.',
'suspense':'A reader’s uncertainty or anticipation about what will happen.',
'character':'A person or figure represented in a narrative or dramatic work.',
'theme':'A central idea a work develops through its choices and events.',
'motivation':'A reason a character chooses to act in a particular way.',
'inference':'A conclusion drawn from details rather than explicitly stated facts.',
'resolution':'The outcome or settlement of a major story problem.',
'simile':'An explicit comparison using like or as.',
'imagery':'Descriptive language that activates sensory imagination.',
'personification':'Giving a nonhuman subject human traits or actions.',
'metaphor':'An implicit comparison that treats one thing as another.',
'symbol':'An object, image, or action that suggests meaning beyond itself.',
'rhyme':'Similarity in stressed ending sounds between words.',
'subtext':'Meaning suggested beneath or beyond the literal words.',
'main idea':'The most important idea developed in a piece of writing.',
'compare':'To examine similarities and differences.',
'data':'Recorded observations, measurements, or values used in analysis.',
'diagram':'A simplified visual representation of parts or relationships.',
'procedure':'A sequence of steps used to carry out a task.',
'sample':'A selected subset of a larger group that is studied.',
'quantify':'To describe or measure using numerical amounts.',
'relationship':'A connection between people, events, factors, or concepts.',
'observation':'Information directly noticed or recorded.',
'corroboration':'Additional independent support for a claim or account.',
'claim':'A statement that can be supported, challenged, or evaluated.',
'uncertainty':'A limit on what is known or how confidently it is known.',
'chronology':'The order in which events happened.',
'verification':'Checking whether a statement is supported and accurate.',
'control':'A factor held constant or compared to isolate an effect.',
'audience':'The readers, listeners, or viewers a communication addresses.',
'sequence':'The order in which events or steps occur.',
'unity':'The quality of details working together to support one main idea.',
'revision':'Rethinking and changing a draft to improve meaning and effectiveness.',
'integration':'Weaving evidence or source material into one’s own explanation.',
'conciseness':'Expressing an idea clearly without unnecessary words.',
'reflection':'Thoughtful examination of an experience or learning process.',
'evaluation':'Judgment using stated criteria and relevant evidence.',
'warrant':'The reasoning that connects a piece of evidence to a claim.',
'proposal':'A plan or recommendation put forward for consideration.',
'purpose':'The intended goal of a text, speech, or action.',
'counterargument':'A reasoned objection or competing argument to a claim.',
'qualifier':'Language that limits how broadly a claim applies.',
'appeal':'A persuasive move toward the values, emotions, or reasons of an audience.',
'reasoning':'The logical process connecting premises, evidence, and conclusions.',
'rebuttal':'A reasoned response to an objection or counterargument.',
'authority':'The relevant expertise, position, or credentials of a source.',
'currency':'How recent and timely a source is for a specific question.',
'attribution':'Crediting an idea, quotation, or finding to its source.',
'query':'A set of words or filters used to search for information.',
'paraphrase':'Restating a source’s idea independently while crediting the source.',
'methodology':'The organized approach and procedures used in research.',
'scope':'The limits of what a study or argument attempts to cover.',
'citation':'A reference that identifies the source of a quotation, fact, or idea.',
'active listening':'Careful attention, questioning, and checking understanding of a speaker.',
'clarification':'Making a meaning or request more specific and understandable.',
'delivery':'The way a spoken presentation is performed and communicated.',
'civility':'Respectful communication even when people disagree.',
'specificity':'Use of particular, concrete details instead of general claims.',
'synthesis':'Combining ideas or evidence into an integrated account.',
'visual literacy':'The ability to interpret and communicate meaning through images and diagrams.',
'organization':'The arrangement of ideas into an understandable sequence and structure.',
}
# Each line: question | exact answer | accepted alternative (optional). Unit order matches RAW.
CUSTOM_FILL = {
'phonics': '''Type the beginning letter shared by bell and boat.|b|
How many spoken syllables does banana have? Enter a number.|3|three
What is the silent first letter in knee?|k|
Which word in the reading rhymes with light?|night|
Write the two-letter prefix in replay that can mean again.|re|re-
Which word root shared by telescope and microscope refers to looking?|scope|
What is the extra final letter in cape that is absent from cap?|e|
What two-letter digraph begins ship?|sh|''',
'fluency': '''Which punctuation mark commonly signals a pause in the reading example?|comma|,
Which reading practice did Eli repeat?|rereading|reading again
Which punctuation mark signaled a question in Ada’s example?|question mark|?
What marks identified separate speakers in Noel’s example?|quotation marks|quotes
What feature of the poem did Kai use as a pacing cue?|line breaks|line break
Which two kinds of details did Zoe practice articulating?|names and numbers|numbers and names
What word refers to connected groups of words read together?|phrases|phrase
What kind of detail did Uma decide to emphasize?|number|figure''',
'vocabulary': '''Which word describes a small, weak light in the case?|glimmer|
Which word in the case means likely but not certain?|probable|
Which word suggested hesitation before agreeing?|reluctant|
Which word means that a resource is limited or in short supply?|scarce|
Which word carries a more approving tone than stubborn?|determined|
Which word root in portable relates to carrying?|port|
Which word has different senses in electricity and rivers?|current|
Which precise verb replaced went quickly?|sprinted|''',
'grammar': '''What punctuation mark commonly precedes a coordinating conjunction in a compound sentence?|comma|,
What is the correct present-tense verb with the subject birds: fly or flies?|fly|
What kind of word must a pronoun refer to clearly?|antecedent|noun
What type of descriptive language was misplaced in the example?|modifier|
What is the name of using matching grammatical forms in a list?|parallelism|
For multiple bakers owning something, does the possessive apostrophe go before or after plural s?|after|after s
What is the grammatical voice of “The student repaired the gate”?|active|active voice
What is the name for improperly joining complete clauses without punctuation?|run-on|run on''',
'fiction': '''What object did Niko discover beside the pier?|map|a map
What material was Tess building her bridge from?|paper|
What was making the tapping noise at the library window?|branch|a branch
What navigation tool did Hugo borrow?|compass|a compass
What was flickering in Jia’s story?|signal light|lantern
What did Milo’s mesh screen keep out?|leaves|
Which part of the garden was left open?|gate|
How many invitations created Eden’s scheduling problem?|2|two''',
'poetry': '''What figurative device explicitly compares things using like or as?|simile|
What color did the remaining light fade into?|blue|
Which nonhuman objects were described as dancing?|leaves|
What repeating sound did Rory hear in the station?|tick|ticking
What object was the river compared to?|mirror|
What empty object became a possible symbol onstage?|chair|
How many lines were in the example poem?|4|four
What part of the script told Noa how to move?|stage direction|stage directions''',
'information': '''How many raised beds were shown in the proposed garden plan?|6|six
How many minutes apart were Route A arrivals in the fictional chart?|20|twenty
How many leftover lunches were reported for Friday?|7|seven
In the route diagram, did water flow from higher ground toward a basin or the reverse?|toward a basin|higher ground toward a basin
What was the first safety step in the repair checklist?|disconnect power|disconnect the power
How many patrons preferred evening library hours in the sample?|18|eighteen
Which bottle listed the larger volume: 500 mL or 750 mL?|750 mL|750
Name one type of organism shown on the wetland poster.|frogs|reeds;insects''',
'evidence': '''What surface condition did Luz observe around the footprints?|wet soil|wet
Where did Ari find the missing paintbrush?|storage|labeled box
What number did the second-week library traffic chart show?|55|fifty five
What object did the hallway recording capture rolling?|cart|rolling cart
What repeated geometric shape characterized the tire tread?|zigzag|zigzag pattern
What time was on the original published meeting notice?|3:30|3 30
What identifying information did the online quotation lack?|author|source
Which variable was not held equal between Jay’s two plants?|sunlight|light''',
'composition': '''What kind of specific detail improved Anika’s thank-you note?|example|specific example
What did Perry add to make instructions easier to follow?|numbered steps|numbers
What kind of sentence did Ruth add to unify her library paragraph?|topic sentence|
What kinds of signals did Luis add to clarify event order?|time signals|transitions
What should follow a quotation so that it supports a claim?|explanation|analysis
Where did Caleb move his request in his revised email?|first paragraph|opening paragraph
What did Sena add to her reflection besides one obstacle?|improvement|one improvement
What was the sound-related limitation Felix added to his review?|unclear dialogue sound|unclear sound''',
'rhetoric': '''How many benches were proposed for the park?|2|two
What kind of trial did Drew propose for the second lunch line?|timed trial|short timed trial
What did Yara replace her alarming slogan with?|clear action and reason|an action and reason
What tool did Ezekiel’s group build to compare priorities?|decision matrix|matrix
How many classmates answered Kemi’s original survey?|8|eight
Which missing resource made the playground street difficult in the example?|shade|
What common unit did Vera use to make a fair price comparison?|price per unit|unit price
Which practical student concern did Micah acknowledge?|transportation|morning transportation''',
'research': '''What important identifying element was absent from the blog page?|author|references
What metadata did Silas check to compare the older and newer articles?|publication dates|dates
Which kind of report did Helena trace the claim back to?|primary report|primary source
What did Avery add to narrow his search along with focused terms?|date range|
What must accompany a paraphrase of another author’s idea?|citation|source credit
How many volunteers were in Juno’s smaller fictional survey?|30|thirty
What aspect of Mae’s research question did she narrow?|scope|focus
What publication information was missing from two references?|years|publication years''',
'speaking': '''What did Hana do to show she understood her partner?|paraphrased|paraphrase
What did Moss ask the group to define for its experiment?|outcome|measurement
What did Jules turn to face during the improved presentation?|audience|
What did Amina restate before disagreeing?|concern|friend’s concern
What example structure did Kian add to his interview answer?|situation action result|situation, action, and result
How many suggestions did Alma listen to at the roundtable?|3|three
What piece of visual evidence did Ty highlight in the presentation?|comparison|three-person change
What did Rosa add to the beginning of the speech besides an issue and claim?|roadmap|plan''',
}
CUSTOM_FILL={k:[tuple((v.split('|')+[''])[:3]) for v in txt.strip().splitlines()] for k,txt in CUSTOM_FILL.items()}
assert all(len(items)==8 for items in CUSTOM_FILL.values())

LEVEL_BANDS = ['emergent','emergent','early','early','developing','developing','independent','independent','intermediate','intermediate','secondary','secondary','secondary','secondary','college','college']

SENTENCE_STARTERS = {
 'emergent':['I see', 'I think', 'The clue is', 'I can tell'],
 'early':['The passage says', 'One detail is', 'I think this means', 'A question I have is'],
 'developing':['A relevant detail is', 'This supports the idea that', 'However, the text does not show', 'My conclusion is'],
 'independent':['The author gives the example', 'This observation suggests', 'A competing explanation could be', 'A stronger inference would be'],
 'intermediate':['The central claim is', 'The strongest textual evidence is', 'This matters because', 'One limitation is'],
 'secondary':['The passage distinguishes', 'The author’s evidence indicates', 'A plausible alternative interpretation is', 'The conclusion should be qualified because'],
 'college':['The inquiry foregrounds', 'The most defensible reading is', 'The warrant linking evidence to claim is', 'An important methodological limitation is'],
}

SKILLS_BY_BAND = {
 'emergent': ('name a detail','use one accurate word','put two events in order','say what is not yet known'),
 'early': ('identify a central idea','notice exact details','write a complete thought','distinguish a guess from a fact'),
 'developing': ('summarize without adding facts','explain cause and effect','revise a sentence','identify a text limitation'),
 'independent': ('analyze a specific choice','connect evidence to inference','organize a coherent paragraph','evaluate a possible alternative'),
 'intermediate': ('trace a claim through evidence','compare plausible readings','organize an analytical response','qualify a generalization'),
 'secondary': ('evaluate an authorial choice','cite and analyze specific evidence','address a counterclaim','revise for precision and cohesion'),
 'college': ('analyze rhetorical and epistemic choices','integrate source evidence responsibly','assess warrants and counterevidence','write with disciplinary precision'),
}

SYNONYMS = {
 'observation':['detail','saw','notice','noticed','observed'], 'inference':['guess','conclusion','interpretation','hypothesis'],
 'limitation':['uncertain','cannot','not prove','unknown','limited'], 'evidence':['proof','detail','clue','support','observation'],
 'argument':['claim','reason','position','conclusion'], 'revision':['edit','improve','rewrite','refine'],
 'audience':['reader','listener','viewers'], 'comparison':['compare','difference','similarity'],
 'clear':['understandable','precise','direct'], 'context':['surrounding','situation','passage'],
 'source':['report','article','document','citation'], 'conclusion':['inference','interpretation','claim'],
}

def level_number(lid):
 if lid=='PK':return -1
 if lid=='K':return 0
 if lid=='C1':return 13
 if lid=='C2':return 14
 return int(lid)

def wc_limit(lid):
 n=level_number(lid)
 if n<1:return 8 if n<0 else 12
 if n<4:return 18+n*6
 if n<7:return 45+(n-4)*15
 if n<10:return 90+(n-7)*30
 return 170+(n-10)*35

def tidy(x):return re.sub(r'\s+',' ',x).strip()

def splitcase(record):
 xs=record.split('|'); assert len(xs)==9, (record,len(xs))
 return dict(title=xs[0],actor=xs[1],place=xs[2],start=xs[3],observation=xs[4],action=xs[5],outcome=xs[6],limit=xs[7],term=xs[8])

def literary_passage(c, strand, band, lid, seq):
 name=c['actor']; place=c['place']; target=c['title']
 p1=f"At {place}, {name} {c['start']}. The important detail was specific: {c['observation']}."
 p2=f"Instead of assuming an answer, {name} {c['action']}. As a result, {c['outcome']}."
 p3=f"There was still a boundary to this conclusion: {c['limit']}. That distinction between what the account shows and what it cannot establish is part of careful reading."
 if band=='emergent':
  return ([f"{name} was at {place}. {name} {c['start']}. {name} learned something important.",
          f"Here is the clue: {c['observation']}. {name} {c['action']}. The story ends with this result: {c['outcome']}. We still do not know everything: {c['limit']}."],
         [f"Show the clue: {c['observation']}.", f"Say what happened next: {c['outcome']}."])
 if band=='early':
  return ([p1,p2,f"What else should a reader ask? {name} learned that {c['limit']}. A careful reader can name the clue and also say what remains unknown."],
         ["Point to the most important detail.","Retell the action and result in order."])
 if band=='developing':
  return ([p1,p2,p3,
          f"The case is called “{target}” because the sequence highlights {c['term']}. Compare the observation with the response: the first is information in the account, while the second is the action taken in response to it."],
         ["Identify the exact evidence before stating a conclusion.","Write two sentences explaining why the limitation matters."])
 if band=='independent':
  return ([p1,p2,p3,
          f"Notice the order of the narrative. First, a situation prompted attention. Next, a concrete observation created a question. Then an action tested or responded to that question. Finally, an outcome changed what the participants knew. The term {c['term']} helps describe a particular technique used in this case.",
          f"A useful summary should neither invent details nor ignore an inconvenient fact. A reader can say that {c['outcome']}, but must also preserve the caveat that {c['limit']}."],
         ["Distinguish a narrated event from an interpretation.","Explain how the final limitation shapes the lesson."])
 if band=='intermediate':
  return ([p1,p2,p3,
          f"A disciplined interpretation starts by separating observation from explanation. In this instructional case, the observation is “{c['observation']}.” The response is that {name} {c['action']}. Those are not interchangeable claims: one records a detail and the other records what a person chose to do.",
          f"The outcome—{c['outcome']}—supports a limited conclusion about the event. A stronger analysis asks why the same evidence might also allow an alternative reading. The answer must keep the qualifier: {c['limit']}.",
          f"To develop a paragraph, state the interpretive claim, introduce a short quotation, analyze how that quotation supports the claim, and end by specifying what would require further verification. The technical term {c['term']} supplies a vocabulary tool; it is not, by itself, evidence."],
         ["Explain the difference between what a text records and what it implies.","Develop one counter-reading without inventing a new fact."])
 if band=='secondary':
  return ([p1,p2,p3,
          f"The constructed narrative “{target}” offers a deliberately small record. Its precise observation—“{c['observation']}”—provides the best anchor for a textual claim. A writer who replaces that sentence with a vague assertion weakens the causal link between the text and the interpretation.",
          f"A second layer of analysis concerns decisions and consequences. {name} {c['action']}, and {c['outcome']}. The sequence may invite readers to praise a choice, but that judgment remains interpretive. The facts in the passage show an action and outcome; they do not independently prove every motive or counterfactual.",
          f"One qualified interpretation might connect {c['term']} with the outcome while acknowledging an alternative. For example, a skeptical reader could ask whether another action would have produced the same result. The evidence is insufficient to answer that counterfactual, especially because {c['limit']}.",
          "Write with disciplined evidence: distinguish direct quotation, paraphrase, inference, and speculation. Use a precise verb to describe what the author establishes, and avoid the words always, never, and proves unless the record genuinely supports them."],
         ["Evaluate what warrants the interpretation and what merely sounds persuasive.","Include a counterinterpretation and a fair response."])
 return ([p1,p2,p3,
         f"This case is a purpose-built instructional text, not an empirical study or historical report. Its usefulness lies in its traceable evidence chain. At the level of description, the passage records: “{c['observation']}.” At the level of agency, it states that {name} {c['action']}. And at the level of reported consequence, it says {c['outcome']}.",
         f"In critical reading, a defensible thesis must identify the scope of its warrant. Here the observation supports a narrow account of the event, whereas a wider causal generalization would demand comparison cases, source provenance, and transparent methods. The explicit limitation—{c['limit']}—is therefore not a decorative disclaimer: it materially constrains the knowledge claim.",
         f"Treat the term {c['term']} as an analytical tool and ask whether applying that term clarifies the mechanisms of the case or merely labels them. A strong response should cite a short, exact textual phrase, then explain why the phrase changes the interpretation rather than assuming the quotation interprets itself.",
         "A rigorous counter-reading should be charitable, falsifiable where possible, and attentive to what the passage leaves unspecified. Propose a modest follow-up question or additional source that might distinguish rival explanations, but do not present imagined results as findings.",
         "For revision, audit each sentence: Is it description, inference, normative assessment, or recommendation? Make transitions signal those distinctions. Prioritize logical validity and evidentiary precision over ornate prose."],
        ["State an interpretive thesis with a clearly delimited scope.","Distinguish textual validity from hypothetical external validity.","Offer a charitable counter-reading with a targeted verification step."])

def teaching(c, strand, band, levelid, seq):
 is_early=band in ('emergent','early')
 mode = dict(STRANDS)[strand] if False else next(s for s in STRANDS if s[0]==strand)
 skill=SKILLS_BY_BAND[band]
 example=f"The passage states: “{c['observation']}.” An accurate inference is that this detail matters to {c['actor']}’s decision; it does not prove anything beyond the specific situation."
 if is_early:
  example=f"The reading tells us: “{c['observation']}.” That is a detail. We can point to it when we answer."
 mentor=[
  {'title':'Read with a purpose','body':f"In this {mode[1].lower()} lesson, watch for {mode[3]}. The central learning move is to {skill[seq%len(skill)]}."},
  {'title':'Worked example','body':example},
  {'title':'Think before answering','body':f"Ask: What does the passage actually say? How did {c['actor']} respond? What does the text leave undecided?"},
  {'title':'Sentence frames','body':'  •  '.join(SENTENCE_STARTERS[band])},
  {'title':'Revision workshop','body':f"Recheck your wording against the exact detail “{c['observation']}”. Explain why that detail matters. Avoid treating “{c['limit']}” as a proven universal rule."},
 ]
 for k in range(3):
  mentor.append({'title':('Independent practice','Apply the pattern','Self-check')[k], 'body':[
   f"Try a new example with the same skill. Read a short text, highlight a precise detail, then write an interpretation that the detail supports. If you have no supporting detail, label the idea as a question.",
   f"In “{c['title']}”, separate these three pieces: observation ({c['observation']}), response ({c['action']}), and outcome ({c['outcome']}). Explain their relationship without inventing an intervening event.",
   f"Before submitting: Did you respond directly? Did you include relevant evidence? Did you explain your thinking? Did you preserve the caution that {c['limit']}? Did you reread and revise for clarity?",
  ][k]})
 return mentor

def questions(c, strand, band, lid, seq, paragraphs):
 actor,obs,action,outcome,limitterm=c['actor'],c['observation'],c['action'],c['outcome'],c['limit']
 dothers=[splitcase(x) for x in RAW[strand] if x!=RAW[strand][seq]]
 dp=dothers[:]
 mcq=lambda n,prompt,options,answer,why,skill:'dummy'
 qs=[]
 def add(typ,prompt,*,answer=None,options=None,alts=None,points=10,reason='',skill='',**kwargs):
  q={'id':f'q{len(qs)+1:02d}','type':typ,'prompt':prompt,'points':points,'skill':skill,'reason':reason}
  if answer is not None:q['answer']=answer
  if options is not None:q['options']=[{'id':f'o{i}','text':s} for i,s in enumerate(options)]
  if alts is not None:q['alternatives']=alts
  q.update(kwargs);qs.append(q)
 def shuffle(opts,correct,j):
  # deterministic answer-position rotation; all options distinct
  arr=[correct]+[x for x in opts if x!=correct][:3]
  assert len(set(arr))==4,(c['title'],arr)
  for _ in range((seq+j+level_number(lid)+3)%4):arr.append(arr.pop(0))
  return arr, f'o{arr.index(correct)}'
 opts,ans=shuffle([d['start'] for d in dp],c['start'],0)
 add('mcq',f'What did {actor} first do in the reading?',options=opts,answer=ans,reason=f'The action is explicitly reported: {actor} {c["start"]}.',skill='retrieve')
 opts,ans=shuffle([d['observation'] for d in dp],obs,1)
 add('mcq','Which detail can you directly verify in the passage?',options=opts,answer=ans,reason=f'The passage records: {obs}.',skill='text evidence')
 opts,ans=shuffle([d['action'] for d in dp],action,2)
 add('mcq',f'How did {actor} respond to the information?',options=opts,answer=ans,reason=f'It says that {actor} {action}.',skill='sequence')
 opts,ans=shuffle([d['outcome'] for d in dp],outcome,3)
 add('mcq','Which result is stated in the account?',options=opts,answer=ans,reason=f'The stated outcome is: {outcome}.',skill='outcome')
 opts,ans=shuffle([d['limit'] for d in dp],limitterm,4)
 add('mcq','Which statement most responsibly limits the interpretation?',options=opts,answer=ans,reason=f'The account makes this limitation explicit: {limitterm}.',skill='critical reading')
 add('fill',f'What technical word does this lesson introduce for closer study?',answer=c['term'],alts=[c['term'].lower()],reason=f'The featured concept is {c["term"]}.',skill='vocabulary')
 # Text-based cloze can be scored without making generated grammar claims
 add('fill',f'Name the character or researcher at the center of this account.',answer=actor,alts=[actor.lower()],reason=f'{actor} is named in the first sentence.',skill='reading detail')
 defs=[TERM_DEFINITIONS[splitcase(x)['term']] for x in RAW[strand]]
 termdef=TERM_DEFINITIONS[c['term']]
 candidates=[termdef]+[v for v in defs if v!=termdef]
 choices,correct=shuffle(candidates[1:],termdef,6)
 add('mcq',f'In English study, what does the term “{c["term"]}” mean?',options=choices,answer=correct,reason=f'{c["term"]}: {termdef}',skill='concept mastery')
 add('short',f'Explain in your own words why the observed detail mattered to {actor}’s choice.',keywords=['detail','action','because'],
  concepts=[{'label':'A concrete observation','terms':[c['term'], 'detail','clue','observation', 'noticed', 'saw']},{'label':'Reason or impact','terms':['because','therefore','so','led','helped','changed','suggested']},{'label':'Reference to the event','terms':[actor, c['action'].split(' ')[0]]}],
  expectedEvidence=[obs],minimumWords=max(8, wc_limit(lid)//3),
  sample=f"The detail that {obs} mattered because it informed the decision to {action}. A careful explanation stays close to the passage.",
  reason='Connect a specific observation with an action; merely naming a topic is not enough.',skill='reasoning')
 add('short',f'What conclusion is supported, and what should the reader avoid claiming about “{c["title"]}”?',keywords=['outcome','limit'],
  concepts=[{'label':'Recognizes outcome','terms':['outcome','result','led','happened','reported']},{'label':'Recognizes uncertainty','terms':['might','may','not','cannot','uncertain','limited','unknown','without','however']},{'label':'Connects textual detail','terms':['passage','detail','text','because','evidence']}],
  expectedEvidence=[outcome, limitterm], minimumWords=max(10,wc_limit(lid)//2),
  sample=f"The passage supports the conclusion that {outcome}. It does not establish a broader rule, because {limitterm}.",
  reason='A warranted inference names what happened and respects the limit of the evidence.',skill='qualified inference')
 # Revision exercise, objective answer supplied with flexible acceptable punctuation variants
 fix=f"{actor} {action} and {outcome}"
 correct=f"{actor} {action}, and {outcome}."
 add('edit',f'Add appropriate capitalization and ending punctuation to this practice sentence: “{fix.lower()}”',answer=correct,
     alternatives=[f"{actor} {action} and {outcome}.",f"{actor} {action}, and {outcome}!"],
     reason='A sentence starts with a capital and ends with an appropriate mark. Comma placement can vary with the clause structure.',skill='editing')
 add('order','Put the information in the same logical sequence as the passage.',steps=[c['start'],obs,action,outcome],answer=[0,1,2,3],reason='Situation → Observation → Response → Result.',skill='chronology')
 # evidence selection is objectively gradable against a passage
 opts,ans=shuffle([d['observation'] for d in dp],obs,5)
 add('mcq','Which quoted detail would best support a claim about what was observed?',options=opts,answer=ans,reason=f'“{obs}” is traceable to the original passage.',skill='quotation')
 # editing diagnostic with a deliberate multiword-only exact answer
 fillprompt,fillanswer,fillalt=CUSTOM_FILL[strand][seq]
 add('fill',fillprompt,answer=fillanswer,alts=fillalt.split(';') if fillalt else [],reason=f'Unit-specific application: {fillanswer}.',skill='subject application')
 add('essay',f'Write a {"short story retelling" if band=="emergent" else "well-developed evidence-based response"} about “{c["title"]}.” Explain what is known, why it matters, and what remains uncertain. Include your own interpretation, not only quotations.',
  points=20, minimumWords=wc_limit(lid),
  referenceText='\n\n'.join(paragraphs),
  concepts=[{'label':'Specific observation','terms':[c['term'],'observation','detail', 'evidence', 'noticed', 'recorded',c['actor']]},
            {'label':'Action and consequence','terms':['action','response','result','outcome','because','led','after','therefore']},
            {'label':'Qualification','terms':['however','although','might','may','cannot','unknown','limitation','uncertain','not','while']}],
  expectedEvidence=[obs,action,outcome],
  rubric=[{'key':'task','label':'Addresses the prompt','weight':.18},{'key':'reason','label':'Explanation and reasoning','weight':.22},
          {'key':'evidence','label':'Textual evidence','weight':.24},{'key':'organization','label':'Organization','weight':.16},
          {'key':'style','label':'Sentence craft and conventions','weight':.12},{'key':'integrity','label':'Independent work and calibration','weight':.08}],
  sample=f"In “{c['title']}”, {actor} {c['start']}. The narrative gives a concrete observation: “{obs}.” This is relevant because {actor} {action}, and {outcome}. The result suggests a connection between observation and response, but it should not be overstated: {limitterm}. A responsible interpretation separates what the text states from the conclusions a reader constructs.",
  reason='An essay needs a claim, accurate textual evidence, explanation, organization and proportionate uncertainty.',skill='extended composition')
 assert len(qs)==15, len(qs)
 return qs

# Art assets are original mini visual lesson maps, drawn as SVG rather than placeholders.
# Different strands receive graphically different relationship diagrams and coherent palettes.
PALETTES = [('#0a1c35','#0d5aa8','#49dce9','#fae3a1'),('#12203b','#6a48af','#8be5ed','#ffcd82'),
            ('#102b33','#167f83','#90e5c7','#f8c987'),('#151f39','#305aa4','#f5ae72','#a5ccff'),
            ('#182338','#9858a6','#ed9fcb','#a5e8ec'),('#132b3d','#2b7f9f','#b7eef9','#ffa884')]

# Early-literacy phonics posters emphasize large, discernible print patterns and
# visual grouping rather than abstract essay/evidence concepts.
EARLY_TILES = [
 (['B','b'],['BELL','BOAT'],'Listen for /b/ at the beginning'),
 (['BA','NA','NA'],['3 CLAPS','3 SYLLABLES'],'Say banana in three beats'),
 (['K','NEE'],['SILENT K','KNEE'],'The k is written but not heard'),
 (['L','IGHT'],['LIGHT','NIGHT'],'Hear the matching ending sound'),
 (['RE','PLAY'],['AGAIN','REPLAY'],'A prefix changes the meaning'),
 (['TELE','SCOPE'],['MICRO','SCOPE'],'Explore related word roots'),
 (['CAP','CAPE'],['SHORT A','LONG A'],'A final e changes the sound'),
 (['SH','IP'],['ONE SOUND','TWO LETTERS'],'The letters sh work together'),
]
def early_phonics_diagram(lesson,unit):
    tiles,hints,caption=EARLY_TILES[unit]
    # Large typographic examples for early readers, with instructional anchors.
    import math
    steps=''.join(f'<g transform="translate({72+i*308} 362)"><rect width="293" height="123" rx="25" fill="#ffffff" fill-opacity=".9"/><circle cx="35" cy="30" r="17" fill="#126d96"/><text x="35" y="36" text-anchor="middle" fill="white" font-family="Arial,sans-serif" font-size="16" font-weight="bold">{i+1}</text><text x="23" y="85" fill="#10365e" font-size="{31 if len(x)>8 else 38}" font-weight="800">{html.escape(x)}</text></g>' for i,x in enumerate((hints+['SAY IT','TRY IT'])[:3]))
    blocks=[]
    left=77
    for idx,part in enumerate(tiles):
        w=285 if len(tiles)==2 else 200
        xx=left+idx*(w+14)
        blocks.append(f'<rect x="{xx}" y="172" width="{w}" height="150" rx="29" fill="#fff" fill-opacity=".95" stroke="#ffe8a5" stroke-width="4"/>')
        blocks.append(f'<text x="{xx+w/2:.0f}" y="278" text-anchor="middle" fill="#145884" font-family="Arial,sans-serif" font-size="{83 if len(part)<4 else 59}" font-weight="900">{html.escape(part)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="570" viewBox="0 0 1200 570" role="img" aria-label="Early reading poster: {html.escape(caption)}">
<defs><linearGradient id="blue" x2="1" y2="1"><stop stop-color="#0d5b97"/><stop offset="1" stop-color="#17a9ab"/></linearGradient><pattern id="stars" width="38" height="38" patternUnits="userSpaceOnUse"><circle cx="18" cy="18" r="2" fill="#fff" opacity=".11"/></pattern></defs>
<rect width="1200" height="570" fill="url(#blue)"/><rect width="1200" height="570" fill="url(#stars)"/>
<circle cx="986" cy="227" r="207" fill="#b4f2f0" opacity=".16"/><circle cx="1040" cy="240" r="140" fill="none" stroke="#fff" stroke-opacity=".29" stroke-width="5"/>
<text x="69" y="52" fill="#e1ffff" letter-spacing="3" font-size="19" font-weight="800">ATLAS · SOUND SCIENTIST</text>
<text x="69" y="119" fill="white" font-size="42" font-weight="850">{html.escape(lesson['caseTitle'])}</text>
<text x="71" y="153" fill="#d0f4f7" font-size="21">{html.escape(lesson['levelName'])} · Read it, say it, and listen to the sound</text>
{''.join(blocks)}
<rect x="755" y="172" width="373" height="150" rx="26" fill="#084571" fill-opacity=".63" stroke="#8ce7e0" stroke-width="3"/>
<text x="782" y="228" fill="#aaffea" font-size="19" font-weight="800">TODAY’S SOUND CLUE</text>
<text x="780" y="274" fill="#fff" font-size="24" font-weight="750">{html.escape(caption)}</text>
{steps}
<text x="70" y="547" fill="#e4fbff" font-size="16">Practice with a grown-up · Point to a word · Say the sounds aloud · Try another example</text>
</svg>'''

def svg_diagram(lesson, c, si, unit, levelid):
 if levelid in ('PK','K') and si==0:return early_phonics_diagram(lesson,unit)
 bg,accent,highlight,gold=PALETTES[si%len(PALETTES)]
 title=html.escape(lesson['title']); term=html.escape(c['term'].upper())
 subtitle=html.escape(f"{lesson['levelName']}  /  {lesson['strandName']}")
 steps=[('NOTICE','Read what happened'),('EVIDENCE','Locate the clue'),('REASON','Explain the link'),('REVISE','Qualify the claim')]
 # Word-wrapped topic-derived caption, with XML-safe shortening
 def wrap(s,maxlen=34):
  words=str(s).split();out=[];line=''
  for w in words:
   if len(line)+len(w)+1>maxlen and line:out.append(line);line=w
   else:line=(line+' '+w).strip()
  if line:out.append(line)
  return out[:3]
 observation=wrap(c['observation'],44)
 action=wrap(c['action'],44)
 shapes=[]
 # independent custom scene structures per strand and unit, deterministic geometries
 for j in range(11):
  theta=(j+unit*.43+si*.19)*.71
  x=830+int(360*math.cos(theta));y=212+int(125*math.sin(theta))
  shapes.append(f'<circle cx="{x}" cy="{y}" r="{12+j%5*4}" fill="{highlight}" fill-opacity=".07"/>')
 if si in (0,2,3):
  for k,ch in enumerate(c['term'][:8].upper()):
   x=812+k*49;y=178+(k%2)*14
   shapes.append(f'<rect x="{x}" y="{y}" width="44" height="51" rx="10" fill="{highlight}" fill-opacity=".11" stroke="{highlight}" stroke-opacity=".28"/>')
   shapes.append(f'<text x="{x+22}" y="{y+34}" fill="#ecf9ff" font-size="24" font-weight="700" text-anchor="middle">{html.escape(ch)}</text>')
 elif si in (4,5,8):
  shapes+= [f'<path d="M780 255 Q920 30 1120 245" fill="none" stroke="{highlight}" stroke-opacity=".3" stroke-width="8"/>',
            f'<path d="M780 255 L1120 245" fill="none" stroke="{gold}" stroke-opacity=".3" stroke-width="4" stroke-dasharray="10 12"/>']
  for k,(x,y) in enumerate([(790,254),(900,123),(1010,128),(1120,245)]):
   shapes.append(f'<circle cx="{x}" cy="{y}" r="{19+k%2*4}" fill="{highlight}" fill-opacity=".22" stroke="{highlight}" stroke-width="2"/>')
 else:
  for k in range(5):
   xx=791+k*87;h=60+(k*29+unit*17)%87
   shapes.append(f'<rect x="{xx}" y="{250-h}" width="49" height="{h}" rx="6" fill="{highlight}" fill-opacity="{.16+k*.06:.2f}"/>')
 # visual map with evidence cards and a four-stage method strip
 cards=''.join(f'<g transform="translate({56+k*285} 418)"><rect width="270" height="104" rx="13" fill="#ffffff" fill-opacity=".065" stroke="#ffffff" stroke-opacity=".2"/><circle cx="26" cy="27" r="14" fill="{accent}"/><text x="26" y="32" text-anchor="middle" fill="white" font-size="13" font-weight="bold">{k+1}</text><text x="50" y="32" fill="{highlight}" font-size="18" font-weight="700">{s[0]}</text><text x="18" y="68" fill="#e6f1fb" font-size="16">{html.escape(s[1])}</text></g>' for k,s in enumerate(steps))
 evidence=''.join(f'<text x="61" y="{242+i*27}" fill="#e8f5fe" font-size="19">{html.escape(s)}</text>' for i,s in enumerate(observation))
 response=''.join(f'<text x="61" y="{344+i*26}" fill="#c6deef" font-size="17">{html.escape(s)}</text>' for i,s in enumerate(action))
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="570" viewBox="0 0 1200 570" role="img" aria-label="Illustrated evidence and reasoning pathway for {title}">
 <defs><linearGradient id="back" x2="1" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="{accent}" stop-opacity=".33"/></linearGradient><pattern id="grid" width="35" height="35" patternUnits="userSpaceOnUse"><path d="M35 0H0V35" fill="none" stroke="white" stroke-opacity=".045"/></pattern></defs>
 <rect width="1200" height="570" fill="url(#back)"/><rect width="1200" height="570" fill="url(#grid)"/>
 <circle cx="950" cy="195" r="198" fill="{accent}" fill-opacity=".07" stroke="{highlight}" stroke-opacity=".19" stroke-width="2"/>
 {''.join(shapes)}
 <text x="57" y="51" fill="{highlight}" font-size="17" font-weight="700" letter-spacing="2.6">ATLAS  •  ENGLISH STUDIO</text>
 <text x="57" y="103" fill="white" font-size="37" font-weight="750">{title[:58]}</text>
 <text x="57" y="141" fill="#b6d9ec" font-size="19">{subtitle}</text>
 <rect x="57" y="160" width="260" height="34" rx="17" fill="{highlight}" fill-opacity=".17" stroke="{highlight}" stroke-opacity=".48"/>
 <text x="75" y="183" fill="{highlight}" font-size="16" font-weight="700">KEY IDEA · {term[:27]}</text>
 <text x="57" y="215" fill="{gold}" font-size="15" letter-spacing="1.5">OBSERVATION</text>{evidence}
 <text x="57" y="320" fill="{gold}" font-size="15" letter-spacing="1.5">RESPONSE</text>{response}
 <path d="M60 400H1140" stroke="#ffffff" stroke-opacity=".20"/>{cards}
 <text x="60" y="553" fill="#a8c7da" font-size="12">Instructional illustration • Original fictional/example material • Not evidence of external events</text>
 </svg>'''
 return svg

def make_lesson(li,level,band,si,strand,unit):
 case=splitcase(RAW[strand][unit])
 lno=level_number(level)
 paragraphs,focus=literary_passage(case,strand,band,level,unit)
 mode=STRANDS[si]
 headline=f"{case['title']} — {mode[1]}"
 lesson={
  'id':f'{level}-{strand}-{unit+1:02}', 'level':level, 'levelName':li[1], 'strand':strand,'strandName':mode[1],
  'unit':unit+1,'index':si*8+unit+1, 'title':headline, 'caseTitle':case['title'],
  'role':mode[2], 'stage':li[2],'band':band,
  'objective':f"Practice {mode[3]} through a traceable classroom case while you {SKILLS_BY_BAND[band][(unit+si)%4]}.",
  'reading':{'label':'Original instructional text','paragraphs':paragraphs,'kind':'Fictional educational scenario / constructed example',
    'notice':f"Core evidence: {case['observation']}", 'limitation':case['limit']},
  'glossary':[{'word':case['term'],'meaning':TERM_DEFINITIONS[case['term']]},
              {'word':'evidence','meaning':'An observable detail or passage quotation offered to support a claim.'},
              {'word':'inference','meaning':'An interpretation based on details, rather than a directly reported event.'},
              {'word':'qualification','meaning':'Language that limits a claim to what the evidence can support.'}],
  'mentor':teaching(case,strand,band,level,unit),
  'focusQuestions':focus, 'writingPlan':{'purpose':'Explain the passage and support a defensible reading',
   'outline':['Make a direct and appropriately limited claim','Introduce an exact detail from the text','Explain the connection between detail and claim','Address one limitation or alternative','Revise word choice, sentence boundaries, and attribution'],
   'writingFrames':SENTENCE_STARTERS[band]},
  'readingTime':max(8,8+len(paragraphs)*2),
  'art':f'illustrations/{level}-{strand}-{unit+1:02}.svg'
 }
 lesson['questions']=questions(case,strand,band,level,unit,paragraphs)
 return lesson,case

def main():
 DATA.mkdir(parents=True,exist_ok=True);ART.mkdir(parents=True,exist_ok=True)
 summary=[]; lesson_count=assignment_count=0
 with (ROOT/'docs'/'ASSIGNMENT_INDEX.csv').open('w',encoding='utf-8',newline='') as af:
  writer=csv.writer(af);writer.writerow(['level','lesson_id','strand','lesson_title','question_id','type','skill','points'])
  for li,level in enumerate(LEVELS):
   lid=level[0];band=LEVEL_BANDS[li];lessons=[]
   for si,s in enumerate(STRANDS):
    for unit in range(8):
     lesson,case=make_lesson(level,lid,band,si,s[0],unit)
     lessons.append(lesson)
     (ART / Path(lesson['art']).name).write_text(svg_diagram(lesson,case,si,unit,lid),encoding='utf-8')
     for q in lesson['questions']:writer.writerow([lid,lesson['id'],s[0],lesson['title'],q['id'],q['type'],q['skill'],q['points']])
   output={'level':lid,'levelName':level[1],'lessons':lessons}
   # ASCII safe embedding against U+2028 and closing script tags in JS.
   js='window.ATLAS_STUDIO_LEVELS=window.ATLAS_STUDIO_LEVELS||{};window.ATLAS_STUDIO_LEVELS['+json.dumps(lid)+']='+json.dumps(output,ensure_ascii=True,separators=(',',':'))+';\n'
   (DATA / ('level_'+lid.lower()+'.js')).write_text(js,encoding='utf-8')
   (DATA / ('level_'+lid.lower()+'.json')).write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
   lesson_count+=len(lessons);assignment_count+=sum(len(x['questions']) for x in lessons)
   summary += [{'id':l['id'],'level':lid,'strand':l['strand'],'unit':l['unit'],'title':l['title'],'role':l['role'],'art':l['art'],'questionCount':len(l['questions'])} for l in lessons]
   print(level[1],len(lessons),'lessons',sum(len(l['questions']) for l in lessons),'assignments')
 manifest={'version':'2.0','levelCount':len(LEVELS),'lessonCount':lesson_count,'assignmentCount':assignment_count,
 'combinedAssignmentCount':assignment_count+1920,'originalCount':1920,'artCount':lesson_count,
 'levels':[{'id':x[0],'name':x[1],'stage':x[2]} for x in LEVELS],
 'strands':[{'id':s[0],'name':s[1],'role':s[2],'focus':s[3]} for s in STRANDS],
 'lessonIndex':summary,
 'notes':'All constructed passages are original educational fiction/examples. Writing scores are provisional unless independently human reviewed.'}
 (DATA/'manifest.js').write_text('window.ATLAS_STUDIO_MANIFEST='+json.dumps(manifest,ensure_ascii=True,separators=(',',':'))+';\n',encoding='utf-8')
 (DATA/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'docs'/'LEARNING_LEVELS.csv').write_text('level,name,band,lessons,assignments\n'+''.join(f'{x[0]},{x[1]},{LEVEL_BANDS[i]},96,1440\n' for i,x in enumerate(LEVELS)),encoding='utf-8')
 print('TOTAL NEW',lesson_count,assignment_count,'ILLUSTRATIONS',len(list(ART.glob('*.svg'))))
 sizes={p:str(sum(x.stat().st_size for x in (SRC/p).rglob('*') if x.is_file())) for p in ['studio-data','illustrations']}
 print('NEW CONTENT BYTES',sizes)

if __name__=='__main__': main()
