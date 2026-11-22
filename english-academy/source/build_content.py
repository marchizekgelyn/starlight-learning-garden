#!/usr/bin/env python3
"""Deterministic educational content generator; no remote API required.
Every lesson contains original local reading, instruction, and 10 gradable assignments.
"""
import json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
LEVELS=[
('PK','Preschool','Early literacy',6),('K','Kindergarten','Beginning reader',8),
('1','Grade 1','Beginning reader',15),('2','Grade 2','Developing reader',22),
('3','Grade 3','Developing reader',35),('4','Grade 4','Independent reader',45),
('5','Grade 5','Independent reader',55),('6','Grade 6','Intermediate',70),
('7','Grade 7','Intermediate',85),('8','Grade 8','Intermediate',100),
('9','Grade 9','High school',120),('10','Grade 10','High school',140),
('11','Grade 11','High school',165),('12','Grade 12','High school',185),
('C1','College I','Academic writing',230),('C2','College II','Advanced composition',280)]

STRANDS=[
('sounds','Sound, Print & Language Systems','🔤','Hear and recognize sounds, words, spelling patterns, and the systems of language.'),
('phonics','Decoding, Fluency & Spelling','📖','Read accurately, decode unfamiliar words, and develop fluent phrasing.'),
('vocab','Vocabulary & Word Formation','🧩','Understand precise meanings, context clues, roots, registers, and word choice.'),
('grammar','Grammar, Syntax & Style','✍️','Build effective sentences and edit conventions from basic to advanced syntax.'),
('fiction','Fiction & Literary Analysis','📚','Interpret characters, conflicts, structure, themes, narrators, and literary choices.'),
('poetry','Poetry, Drama & Figurative Language','🎭','Recognize sound, rhythm, imagery, metaphor, voice, and performance.'),
('info','Informational & Technical Reading','🔎','Analyze explanatory and technical texts, diagrams, purposes, and structures.'),
('evidence','Close Reading & Textual Evidence','🧭','Make inferences, distinguish evidence and claims, and support interpretations.'),
('writing','Writing Process & Revision','📝','Plan, draft, organize, edit, revise, and reflect on effective prose.'),
('argument','Argumentation & Rhetoric','⚖️','State claims, provide reasons and evidence, address alternatives, and analyze persuasion.'),
('research','Research, Media & Citation','🗂️','Ask questions, locate reliable sources, synthesize findings, and credit others.'),
('speaking','Speaking, Listening & Communication','🗣️','Listen actively, speak clearly, discuss ideas, and adapt to an audience.')]

# Deliberately hand-authored grade-specific targets: 16 levels x 12 strands.
SKILLS={
'sounds': ['Recognize a first sound in a spoken word','Hear syllables, rhymes, and spoken word boundaries','Blend and segment individual phonemes','Recognize vowel teams and common spelling patterns','Explain how syllable patterns guide pronunciation','Compare stressed and unstressed syllables','Use morphology and sound patterns to check decoding','Distinguish phonemes, graphemes, and allophones','Explain dialect variation without judging speakers','Analyze spelling changes across English history','Examine register and phonological variation','Explain how audience influences spoken pronunciation','Compare orthographic systems and sound changes','Evaluate claims about correct pronunciation','Analyze phonology, orthography, and linguistic variation','Evaluate a small linguistic data set and its methodological limits'],
'phonics':['Match letters with familiar spoken sounds','Blend short-vowel consonant-vowel-consonant words','Decode consonant blends and digraphs','Read vowel patterns and multisyllabic words','Apply syllable division and inflectional endings','Decode prefixes, suffixes, and unfamiliar forms','Read multisyllabic academic terms smoothly','Improve phrasing, accuracy, and reading rate','Examine reading fluency and interpretive pacing','Explain how morphology supports efficient decoding','Analyze ambiguity caused by word boundaries','Compare prosody across narrative and persuasive texts','Evaluate how punctuation shapes oral interpretation','Examine reader adaptation to technical vocabulary','Explain fluency, prosody, and comprehension interactions','Critique evidence and limitations in reading assessment'],
'vocab':['Name and describe familiar objects','Sort words into everyday meaning groups','Infer meaning from a nearby clue','Use multiple-meaning words in context','Use prefixes, suffixes, and common roots','Distinguish shades of meaning and connotation','Study Greek and Latin word parts','Use context, morphology, and reference tools together','Analyze denotation, connotation, and register','Analyze nuance, irony, and figurative meanings','Interpret discipline-specific vocabulary','Explain how diction changes tone','Compare semantic shifts across time and context','Use precise vocabulary in analytical writing','Analyze lexical choices in scholarly prose','Critique terminology and operational definitions'],
'grammar':['Recognize a complete spoken idea','Identify nouns, verbs, and ending punctuation','Build statements, questions, and compound sentences','Use pronouns and regular agreement','Combine and expand sentences with modifiers','Control verb tense and subject-verb agreement','Use clauses, conjunctions, and clear references','Revise sentence variety and punctuation','Distinguish independent and dependent clauses','Edit modifiers, parallelism, and pronoun references','Use semicolons and complex syntax effectively','Control emphasis through sentence structure','Analyze stylistic syntax and rhythm','Edit for precision, cohesion, and voice','Revise sophisticated academic sentences','Analyze syntax, genre conventions, and stylistic tradeoffs'],
'fiction':['Retell a story with first, next, and last','Identify a character, setting, and event','Describe a character using actions','Explain plot, problem, and solution','Compare characters and point of view','Infer a theme from recurring details','Analyze perspective, conflict, and change','Analyze narrative structure and characterization','Compare setting, symbolism, and theme','Analyze unreliable narration and irony','Interpret motif, characterization, and ambiguity','Compare literary perspectives across texts','Evaluate form, context, and literary interpretation','Construct a sustained close-reading argument','Compare critical approaches to literature','Defend a nuanced interpretation against alternatives'],
'poetry':['Notice repeated sounds and rhyming words','Hear rhythm and repeating words','Identify sensory words and simple comparisons','Recognize similes and personification','Compare literal and figurative meanings','Explain imagery, stanza, and line breaks','Analyze figurative language and speaker','Examine tone, repetition, and sound pattern','Explain symbolism, rhythm, and allusion','Analyze dramatic dialogue and subtext','Interpret extended metaphor and ambiguity','Evaluate voice, imagery, and form','Analyze how form shapes argument and emotion','Compare poetic and dramatic conventions','Perform a close reading of sound and form','Evaluate interpretive claims about poetic structure'],
'info':['Recognize a label, sign, or factual detail','Identify a topic and key fact','Use headings, pictures, and key details','Explain a main idea with supporting facts','Compare cause/effect and sequence structures','Summarize and compare explanatory texts','Read diagrams, explanations, and domain terms','Evaluate text structure and the role of examples','Distinguish explanation from speculation','Synthesize concepts across two explanations','Evaluate methodology and definitions','Read technical descriptions and limitations','Assess how visuals represent data','Evaluate competing explanations and scope','Analyze methods, assumptions, and findings','Critique technical exposition and inferential validity'],
'evidence':['Point to a detail that answers a question','Find a sentence that shows what happened','Use one detail to explain a simple inference','Distinguish a fact from a guess','Quote or paraphrase a supporting detail','Select strong evidence and explain its relevance','Explain how evidence supports an interpretation','Compare direct quotations and paraphrases','Evaluate inferences and counterevidence','Distinguish correlation, cause, and assertion','Analyze how framing affects evidence','Evaluate source limitations in literary claims','Synthesize and qualify competing interpretations','Identify warrants and gaps in textual arguments','Build a defensible evidence-based interpretation','Evaluate assumptions, alternatives, and warrants'],
'writing':['Draw or dictate a beginning, middle, and end','Write a complete sentence on one idea','Plan, draft, and reread a short paragraph','Organize a paragraph with a topic sentence','Revise clarity, sequence, and sensory detail','Develop paragraphs with transitions','Use introduction, body, and conclusion','Plan and revise multi-paragraph writing','Evaluate cohesion, unity, and transitions','Revise for audience, precision, and purpose','Develop analytical paragraphs with evidence','Use peer feedback and revision priorities','Control a sustained line of reasoning','Revise whole-text coherence and style','Write and revise a source-aware academic essay','Conduct substantive revision using editorial criteria'],
'argument':['Give a preference and one reason','Give a claim with because','State an opinion and support it with an example','Distinguish a reason from an unrelated detail','Write a claim, reasons, and conclusion','Use examples and recognize another view','Support claims with relevant evidence','Distinguish claim, evidence, and reasoning','Write a counterclaim and respectful rebuttal','Identify rhetorical appeals and assumptions','Analyze fallacies without dismissing valid evidence','Assess ethical and emotional appeals','Develop a qualified argument and rebuttal','Evaluate logical structure and audience','Build an academic argument with counterevidence','Evaluate argument quality and limitations rigorously'],
'research':['Ask a question about something observed','Compare two simple information sources','Find a fact and name where it came from','Use a source title and author when available','Distinguish firsthand evidence and retelling','Take notes in your own words','Gather sources and record basic citations','Check authorship, date, and supporting evidence','Distinguish claims, sources, and misinformation','Synthesize multiple reliable sources','Use search strategies and annotation','Apply MLA/APA citation concepts','Evaluate methods, bias, and source credibility','Develop a research question and annotated bibliography','Write a synthesis with attribution and citation','Design and critique a research-based literature review'],
'speaking':['Take turns and listen for one idea','Ask and answer a relevant question','Retell an idea in sequence','Speak clearly and build on a partner’s comment','Summarize a discussion fairly','Use notes and visual support in a talk','Adapt speaking to audience and purpose','Ask clarifying questions and paraphrase','Evaluate claims in a spoken presentation','Present a structured evidence-based explanation','Use discussion norms to test interpretations','Analyze media choices and audience effects','Lead a fair seminar discussion','Give a concise professional presentation','Design a research presentation with clear visuals','Critique a presentation for ethics, clarity, and evidence']}
assert all(len(x)==len(LEVELS) for x in SKILLS.values())

# Original instructional examples and strategies by strand (not scraped source text).
GUIDES={
'sounds':('A spoken word is made of sounds; print represents language with letters and combinations of letters. A phoneme is a contrastive speech sound. A grapheme is a written symbol or symbol group. English spelling is patterned, but spelling and sound are not identical.','Say “ship” slowly: /sh/ /i/ /p/. The letters s and h jointly represent the first sound. Pronunciation differences among dialects are systematic, not evidence of poor intelligence.','Listen, segment, connect sounds to print, then test your interpretation in a meaningful sentence.'),
'phonics':('Decode by connecting spelling patterns to sounds, blending, and checking the resulting word against context. Fluency also requires accuracy, phrasing, and expression; reading quickly without comprehension is not the goal.','In “unhelpful,” identify un- + help + -ful. Read the chunks, blend them, and check meaning. For oral fluency, pause at a comma rather than treating it as an unrelated symbol.','Mark unfamiliar word parts, blend, reread the whole sentence, and summarize what it means.'),
'vocab':('Use context, word parts, grammatical role, and a reliable reference to establish meaning. Definitions should fit the sentence rather than being chosen only because they are familiar.','“The garden was arid; even drought-resistant plants needed water.” Arid means very dry. The surrounding clause supports the definition. “Confident” and “arrogant” overlap but differ in connotation.','Locate the clue; test a meaning; substitute it back into the original sentence.'),
'grammar':('A sentence has a structure. Subjects, verbs, phrases, clauses, and punctuation help readers understand relationships. Revise errors by checking agreement, references, coordination, and emphasis.','“Because the rain stopped.” is a fragment in formal prose. “Because the rain stopped, we went outside.” is complete. In “The students revise,” the plural subject takes revise, not revises.','Find the main clause, locate modifiers, and read the sentence aloud to check clarity.'),
'fiction':('A literary interpretation connects textual details to choices about character, narrator, setting, structure, and theme. Distinguish what happens in a story from what the story may imply.','If a character returns a lost key despite needing money, the action can support an inference about honesty. One act is evidence, but a richer interpretation considers the entire story.','Identify an action, explain its significance, and consider an alternative reading.'),
'poetry':('Poems and plays use sound, pacing, imagery, figurative language, and line or stage structure to create meaning. A metaphor creates a comparison without requiring literal identity.','“The streetlights were stars on the road” is a metaphor: streetlights are compared to stars. Ask what brightness, distance, or hope this comparison contributes.','Read aloud; notice repeated or surprising language; connect form to effect.'),
'info':('Informational writing explains the world through definitions, examples, structures, and evidence. Identify what a passage states, how it is organized, and which claims are limited by the evidence.','A passage stating “Rain filled the basin, then the water entered the soil” follows sequence. A diagram may add useful detail, but its labels and units still require interpretation.','Locate the central explanation, map supporting ideas, and check the source of each claim.'),
'evidence':('An inference is a conclusion supported by observations, not a guess presented as fact. Evidence must be accurate, relevant, and explained. Quotations and paraphrases should preserve the author’s meaning.','“The lamp was still warm” may support a recent-use inference, but does not alone establish who used it. Cite the observation, explain the reasoning, and name uncertainty.','Claim → cited detail → reasoning → limitation or competing explanation.'),
'writing':('Writing improves through planning, drafting, reading for a reader’s needs, and focused revision. Revise meaning and organization before spending all your time on punctuation.','Draft: “It was good.” Revision: “The library stayed open after school, giving students a quiet place to study.” The revision names the subject and significance.','Plan one purpose; draft a clear beginning, development, and ending; revise for clarity.'),
'argument':('An argument is a justified claim, not merely a strong opinion. Distinguish claims, evidence, warrants, counterarguments, and rhetorical appeals. Good reasoning explains why evidence supports the conclusion.','Claim: “The park should add shade.” Evidence: “Visitors reported heat exposure.” Warrant: “Shade lowers direct sun exposure.” A complete argument acknowledges costs and alternatives.','State a claim, give specific evidence, explain its relevance, and address a fair objection.'),
'research':('Research starts with an answerable question, reliable sources, careful notes, synthesis, and attribution. A source’s authorship, date, methods, and possible bias affect what it can establish.','A city report may document bus ridership; a student interview can add experience but cannot establish citywide ridership alone. Record the title, author or organization, date, and location of information.','Ask, find, evaluate, take notes in your own words, compare, and cite.'),
'speaking':('A clear presentation has an audience, purpose, organization, and relevant evidence. Active listening involves restating meaning accurately, asking thoughtful questions, and responding respectfully.','Instead of “That is wrong,” try “I heard your claim that the garden needs more water. What measurement supports it?” The second response tests evidence without attacking the person.','Prepare an opening, supporting points, and a conclusion; listen; confirm understanding.')}

# Distinct scenarios within each strand: four developmental bands, each with factual anchors.
# Fields: title | actor | setting | action | observation | cause | result | limitation | next | word | meaning | claim.
CASE_ROWS={
'sounds':[
'The Sounds on the Walk|Mia|school playground|said the sounds at the start of sun and sand|both words began with the same /s/ sound|she listened to the first sound|Mia found two matching sounds|not every word with s has the same sound|try finding a word that begins with /m/|rhyme|words with matching ending sounds|listening carefully helps us notice sounds',
'Word Patterns on the Wall|Jordan|classroom word wall|grouped words by their shared vowel patterns|rain and train shared ai, while ran did not|written patterns help predict pronunciations|the group decoded several unfamiliar words|some spellings have more than one pronunciation|test the pattern using a dictionary|pattern|a repeated form or arrangement|checking patterns and context improves decoding',
'The Student Speech Survey|Ari|middle school language club|recorded different pronunciations of the same word|students pronounced some vowels differently but understood one another|pronunciation varies across communities and contexts|the club described systematic differences without ranking speakers|a small club cannot represent every dialect|sample speakers from more communities|dialect|a language variety with systematic features|language variation is patterned and should not be treated as a defect',
'The Orthography Seminar|Noor|college linguistics seminar|compared sound changes with surviving spelling conventions|several words kept spellings after pronunciation changed|written conventions can persist longer than spoken habits|the seminar separated historical explanation from present-day judgment|examples alone do not establish a universal rule|consult historical dictionaries and phonological corpora|orthography|the conventional spelling system of a language|speech, writing, and social convention interact in complex ways'],
'phonics':[
'Sam and the Map|Sam|reading corner|sounded out map and tap one sound at a time|the sounds joined to make whole words|blending connected letters to speech|Sam read two new words|one memorized example does not prove mastery|try the new word cap|blend|to combine sounds into a spoken word|sound-by-sound decoding can unlock new words',
'The Long Word Challenge|Isabel|library reading group|split the word impossible into useful parts|im, possible, and word meaning supported a correct reading|morphemes made a long word easier|Isabel read the sentence smoothly after practice|not every visible letter group is a morpheme|verify an unfamiliar word in context|morpheme|the smallest meaningful unit in language|word parts and context can work together in reading',
'Fluency Is More Than Speed|Leo|student reading studio|recorded a paragraph once quickly and once with phrasing|listeners better understood the version with meaningful pauses|expression and syntax helped show relationships|Leo revised where he paused at punctuation|one reading does not measure long-term growth|compare comprehension after repeated readings|prosody|the rhythm, stress, and intonation of speech|fluent reading joins accuracy with meaningful phrasing',
'Reading Assessment Laboratory|Ren|university literacy seminar|compared decoding accuracy, reading rate, and comprehension|a rapid reader still missed an important inference|one metric cannot represent a complex ability|the group recommended using several measures together|one classroom sample may not generalize|repeat the evaluation with diverse texts|validity|how well evidence supports a particular interpretation or use|responsible reading assessment requires multiple kinds of evidence'],
'vocab':[
'The Picture Basket|Ada|preschool reading table|sorted an apple, a pear, and a spoon into groups|the apple and pear were fruits but the spoon was not|word groups depend on meaning|Ada described the objects with clearer words|a word may belong to several useful groups|sort the objects by color instead|category|a group sharing a feature|precise words help us describe the world',
'The Unfamiliar Garden Word|Rosa|community garden class|read the sentence about arid ground and thirsty plants|the plants needed extra water because the soil was dry|a nearby clue explained the difficult word|Rosa inferred the meaning of arid|not every context clue is complete|confirm the word in a dictionary|arid|very dry|context helps readers infer unfamiliar vocabulary',
'The Language Choice Debate|Dylan|school newspaper room|compared calling a decision firm versus stubborn|the two words implied different attitudes toward the same action|connotation influences readers beyond dictionary meaning|the editors chose wording that matched their evidence|a word’s effect depends partly on audience|test the headline with several readers|connotation|an associated feeling or idea beyond literal meaning|word choice shapes tone and interpretation',
'The Definition Audit|Sana|university methods course|compared competing definitions of the word success|different definitions produced different findings in the same data|measurements depend on how terms are operationalized|the team rewrote its key definitions before making claims|a definition may still omit important dimensions|compare results under another reasonable definition|operationalize|to specify how a concept will be observed or measured|rigorous writing defines contested terms before drawing conclusions'],
'grammar':[
'The Sentence Repair Shop|Eli|classroom sentence table|added a missing action to the words The dog|the complete sentence “The dog runs” expressed a complete idea|the added verb supplied an action|Eli wrote a sentence with an ending period|some complete sentences have a different structure|try turning the sentence into a question|verb|a word expressing an action or state|sentence structure helps readers follow an idea',
'The Clause Connector|June|classroom writing workshop|connected two ideas about rain with because|Because it rained, the game moved indoors made the reason clear|the conjunction expressed a cause|June replaced two choppy statements with one connected sentence|a long sentence can still be unclear|check whether each clause has a clear role|clause|a group of words containing a subject and verb|joining clauses carefully clarifies relationships',
'The Modifier Puzzle|Tomas|school editing team|revised a sentence that placed a modifier beside the wrong noun|the first draft implied that a backpack was running|a misplaced modifier changed the apparent meaning|the team rewrote the line so the student was clearly running|reader context may sometimes rescue an awkward sentence|test the revision without its surrounding paragraph|modifier|a word or phrase that describes or limits another element|syntax affects both accuracy and style',
'The Academic Style Clinic|Mira|college writing center|compared two versions of a technical explanation|the revised version made the agent and causal relationship explicit|long nominal phrases had obscured who did what|readers identified the conclusion more accurately|simplification can erase necessary technical precision|ask specialist and general readers to review the draft|nominalization|a noun formed from a verb or adjective|academic style should balance precision, agency, and readability'],
'fiction':[
'The Lost Red Mitten|Nia|snowy schoolyard|returned a red mitten to its owner|the owner smiled and thanked Nia|Nia knew someone else needed it|the class found the mitten’s owner|one helpful act does not describe everything about Nia|read another story about a helpful choice|character|a person or other agent in a story|actions can help readers understand characters',
'The Hidden Key|Owen|old town library|returned a key even though he hoped it would open a secret drawer|the librarian revealed that the key belonged to the archive|Owen valued being trusted more than getting a prize|the librarian invited Owen to help catalog books|the narrator does not tell us every private thought|reread the ending from the librarian’s perspective|motive|a reason that explains an action|character choices create conflict and reveal values',
'The Bridge at Dusk|Kira|flooded riverside town|crossed the bridge to deliver a warning|the narrator repeated details of the dark water but omitted the bridge inspection|the restricted viewpoint increased uncertainty|readers questioned whether the journey was wise|the narrative offers only one witness|compare the account with another character’s version|narrator|the voice that tells the story|the narrator’s choices shape what readers believe',
'The Archive of Unsent Letters|Elena|literature research seminar|compared contradictory letters left by a fictional narrator|each letter cast the same departure as both courage and betrayal|memory and self-interest shaped the versions|the class proposed two defensible interpretations|neither letter independently proves the whole history|test both interpretations against the narrative ending|ambiguity|a capacity for more than one plausible interpretation|literary meaning may remain debatable even when evidence is carefully examined'],
'poetry':[
'The Rain Song|Bo|music circle|clapped each time the word drip returned|the repeating word made a steady rhythm|repetition helped the class hear the pattern|the class performed a short rain poem|not every poem has a regular beat|read the poem once quietly and once aloud|rhythm|a pattern of beats or movement|sound patterns shape how language feels',
'The Lantern Poem|Jules|school poetry workshop|called the lantern a small sun in a poem|the comparison made the lantern seem warm and bright|the metaphor connected two unlike things|readers pictured light in a dark path|a metaphor may suggest more than one feature|replace the metaphor and compare the mood|metaphor|a comparison that describes one thing as another|figurative language creates layers of meaning',
'The Stage Without Words|Amal|youth theatre rehearsal|studied a scene with long pauses between two characters|silence suggested tension that no line stated directly|timing influenced how the audience inferred emotion|the cast changed pauses to test different interpretations|audiences may read the same pause differently|ask viewers to describe the scene’s mood|subtext|meaning suggested but not directly spoken|performance choices can carry meaning beyond dialogue',
'The Line Break Experiment|Priya|advanced poetry seminar|moved a line break in a poem about a delayed return|the changed pause shifted emphasis from hope to uncertainty|lineation controls when readers encounter key words|the seminar developed two close readings|oral performance may change the effect of a written break|compare the layout with recorded readings|lineation|the arrangement of poetic lines|poetic form can shape interpretation without changing words'],
'info':[
'How Seeds Grow|Max|classroom window|put a bean in damp soil and watched it|a small shoot appeared after several days|water and suitable conditions supported germination|the class recorded the plant’s growth|one bean cannot show every growing condition|try observing several seeds|germination|the beginning of growth from a seed|careful observation helps explain natural changes',
'The City Water Guide|Talia|town science fair|made a diagram showing water moving from rainfall into streams|arrows showed how runoff connected the hillside to a river|the diagram explained a sequence of movement|visitors traced the route with their fingers|the drawing did not show quantities of water|add measured amounts to the diagram|runoff|water flowing over land toward lower areas|visual explanations should be read with their stated limits',
'The Energy Comparison|Quinn|school engineering club|compared energy use in two classroom lighting setups|one setup used less electricity during the same test interval|the test controlled observation time|the club proposed a larger trial|the conditions differed from every possible classroom|repeat the test across more rooms|variable|a feature that may change in a study|technical explanations depend on measurements and assumptions',
'The Model and Its Limits|Hana|university environmental seminar|compared predictions from two watershed models|their estimates diverged under unusual rainfall assumptions|different simplifications produced different outputs|the group reported a range rather than one certain forecast|neither model was verified for every extreme event|collect additional observations during storms|model|a simplified representation used to explain or predict|strong technical writing states what a model does and does not show'],
'evidence':[
'Whose Footprints?|Luz|garden path|noticed fresh muddy footprints near a watering can|the ground was wet and showed small shoe marks|recent rain could also have made the mud|Luz said someone may have walked there|footprints alone did not identify who visited|ask an adult before making a claim|evidence|information that supports an idea|a clue can support a possibility without proving it',
'The Missing Lunchbox|Kai|school hallway|checked the lost-and-found log before guessing what happened|a lunchbox was recorded at noon|the written entry was more reliable than a rumor|Kai found the lunchbox in the office|the log did not describe who brought it in|ask staff for the remaining detail|inference|a conclusion based on evidence and reasoning|claims should match what evidence can support',
'The River Report|Avery|student science desk|compared an eyewitness account with a river sensor chart|both sources indicated rising water but at different times|their methods captured different observations|the team separated measurements from interpretation|a sensor may malfunction and a witness may forget details|check the calibration and exact timestamps|corroborate|to support a claim with additional evidence|multiple independent sources can strengthen but not guarantee a conclusion',
'The Competing Explanations|Iris|college evidence workshop|evaluated two accounts of a sudden attendance decline|one account cited a schedule change and another cited transportation problems|each explanation drew on incomplete data|the group withheld a single causal conclusion|correlation did not establish a cause|seek records that distinguish the hypotheses|warrant|the reasoning connecting evidence to a claim|strong interpretation tests rival explanations and hidden assumptions'],
'writing':[
'The Three-Part Story|Ben|story circle|told how a toy boat was built, sailed, and recovered|listeners followed the beginning, middle, and end|the events were in a clear order|Ben retold the story in three sentences|some stories need more detail to be understood|add one detail about the water|sequence|the order in which events happen|clear order makes writing easier to follow',
'The Neighborhood Newsletter|Maya|community writing group|revised a vague paragraph about a garden|the new paragraph named who planted vegetables and why|specific details answered readers’ questions|the final newsletter was easier to understand|extra facts can still distract from the main point|ask another reader what detail remains unclear|revision|changing a draft to improve its meaning or effectiveness|revision strengthens ideas, not only punctuation',
'The Museum Explanation|Caleb|school exhibit team|reorganized a draft about a historical artifact|the revised draft moved background before analysis|readers now understood the context before the interpretation|the exhibit received more useful questions|reader reactions are not a complete proof of accuracy|test the text with people new to the topic|coherence|clear logical connection among parts of a text|good organization guides readers through reasoning',
'The Journal Revision|Wren|university writing workshop|restructured an essay after feedback about an unsupported conclusion|the new draft added evidence and qualified the thesis|revising the central claim improved the paper more than surface edits|the final argument addressed a significant limitation|feedback can conflict and requires judgment|compare the revision against the assignment criteria|substantive revision|changes to ideas, evidence, structure, or reasoning|effective editing prioritizes the problems most important to meaning'],
'argument':[
'The Favorite Book|Pia|reading rug|said she liked the animal book because its pictures were clear|her reason connected to her preference|the pictures helped her follow the story|a friend understood her choice|another child may prefer a different kind of book|ask the friend for a reason too|reason|an explanation of why someone thinks or acts|a preference becomes clearer when supported by a reason',
'The Playground Shade Proposal|Noah|student council|asked for an extra shade canopy and showed how hot the play area became|the temperature record gave a relevant reason|shade would reduce direct sun exposure|the council agreed to request cost estimates|cost and placement still needed examination|compare several possible shade locations|claim|a position that can be supported with reasons|an effective argument connects evidence to a practical proposal',
'The Device Policy Debate|Evan|school debate club|argued for a limited device policy using classroom observations|opponents raised legitimate accessibility needs|a good policy must weigh benefits and tradeoffs|the club proposed explicit exceptions and review|observations from one classroom were insufficient for a universal rule|gather perspectives from affected students|counterargument|a reason or claim that challenges another argument|acknowledging an objection can make an argument more credible',
'The Public Transit Editorial|Selene|college rhetoric seminar|analyzed a transit editorial combining statistics and personal narratives|numerical trends and emotional stories served different rhetorical roles|different evidence types can influence audiences differently|the class rewrote the argument with a clear causal warrant|neither a moving story nor a chart automatically proves policy impact|compare the editorial with independent ridership research|rhetoric|the strategic use of communication for an audience and purpose|persuasion should be evaluated for reasoning, evidence, and ethical framing'],
'research':[
'The Question Jar|Finn|classroom science table|asked why one plant was taller than another|the children offered several possible explanations|an answerable question prompted closer observation|the class decided to measure the plants|one look could not explain the difference|measure height over several days|question|something someone asks to learn or understand|careful questions can start research',
'The History Notebook|Leah|local history club|compared an old newspaper with a museum timeline|the sources described the same event with different details|sources may use different records and purposes|Leah recorded both source titles rather than blending them silently|neither source independently answered every question|look for an original event record|source|a person, document, or object supplying information|researchers should track where each claim comes from',
'The Viral Image Check|Miles|media literacy class|traced a widely shared photograph to its original publication|the image caption had been changed years after the photo was taken|the upload date differed from the event date|the students corrected their initial interpretation|the origin alone did not settle every claim in the post|check independent reporting about the event|provenance|the documented origin or history of an item|source context matters when evaluating online claims',
'The Research Synthesis Desk|Aisha|college library seminar|compared peer-reviewed studies with different samples and measures|their results were not directly interchangeable|differences in methods affected the strength of conclusions|Aisha qualified the synthesis rather than averaging incompatible findings|publication status does not guarantee that a study is correct|inspect methods and limitations in each article|synthesis|combining findings while preserving important differences|credible research communicates methods, attribution, and uncertainty'],
'speaking':[
'The Listening Circle|Rae|classroom rug|waited for a classmate to finish before asking about a story|the classmate felt heard and gave another detail|taking turns made the exchange clearer|both children could retell the main idea|a polite turn alone does not prove understanding|repeat the main idea in your own words|listen|to attend carefully to what someone says|listening and relevant questions strengthen conversations',
'The Weather Presentation|Zoe|school assembly|explained a rainfall chart using a beginning, middle, and ending|listeners understood the axes after Zoe named the units|clear organization and labels supported the talk|students asked more precise questions|the chart covered only one month|prepare a comparison with another month|audience|the people who receive a message or presentation|presenters should adapt evidence and language to listeners',
'The Difficult Discussion|Nolan|student community forum|paraphrased an opponent’s proposal before disagreeing|the other speaker confirmed the paraphrase was accurate|restating a view reduced misunderstanding|the group identified an actual point of disagreement|agreement on wording did not resolve the policy question|ask what evidence would change either view|paraphrase|to restate meaning in different words|fair discussion tests ideas while representing others accurately',
'The Conference Briefing|Imani|university research symposium|presented a model with a visual showing uncertainty intervals|the audience distinguished measured results from forecast ranges|clear labels reduced misleading certainty|the discussion focused on assumptions rather than speculation|a slide cannot replace access to methods and underlying data|publish a concise methods summary with the talk|qualification|a condition or limitation placed on a statement|ethical presentations make assumptions and uncertainties visible']
}

assert all(len(records)==4 for records in CASE_ROWS.values())


# Skill-specific microchecks: a distinct application task and typed term for each strand/band.
# format: question|correct|wrong1~wrong2~wrong3|fill question|fill answer|explanation
SKILL_DRILLS={
'sounds':[
'Which words start with the same sound?|sun and sand|sun and moon~sand and dog~cat and sun|Type the first letter in sun.|s|Sun and sand begin with the /s/ sound.',
'Which written letters form a common vowel team?|ai in train|tr in train~rn in train~t in train|Type the vowel team in rain.|ai|In rain and train, the written ai commonly represents a long a sound.',
'Which term names a regional or social variety of language?|dialect|typo~paragraph~punctuation|Type the word for a language variety.|dialect|Dialects have systematic vocabulary, grammar, and pronunciation features.',
'What is orthography?|a conventional system of spelling|the length of a single sentence~the speed of a reading voice~a list of literary themes|Type the term for a conventional spelling system.|orthography|Orthography studies how written forms represent language.'],
'phonics':[
'What word do /m/ /a/ /p/ make when blended?|map|mop~tap~nap|Blend /s/ /u/ /n/. Type the word.|sun|Blend sounds in order, then check the result.',
'Which word contains the prefix un-?|unhappy|happy~happen~perhaps|Type the prefix meaning not in unhappy.|un|A prefix is attached to the beginning of a base.',
'What does prosody include?|stress, rhythm, and intonation|only the number of printed words~only silent reading speed~the number of chapters|Type the term for meaningful reading rhythm and intonation.|prosody|Prosody helps oral reading convey structure and meaning.',
'Which is the strongest reading assessment?|multiple measures of accuracy, rate, and understanding|reading rate alone~one memorized passage~a score without a stated purpose|Type the term for how well a measure supports its intended use.|validity|No single reading measure represents all dimensions of comprehension.'],
'vocab':[
'Which objects are fruits?|apple and pear|spoon and shoe~cup and plate~pencil and ruler|Type the category for apple and pear.|fruit|Word categories are based on shared meanings.',
'If ground is arid, it is _____.|very dry|full of water~very cold~made of stone|Type the word meaning very dry.|arid|A clue about thirsty plants supports the meaning of arid.',
'Which pair most clearly differs in connotation?|firm and stubborn|one and two~red and blue~above and below|Type the term for feelings associated with a word.|connotation|Connotation adds evaluative associations to denotation.',
'Which technique clarifies an unclear research term?|define how it will be measured|repeat the term without explanation~avoid naming the variables~assume everyone agrees|Type the term meaning specify how a concept is measured.|operationalize|Operational definitions reduce ambiguity in empirical writing.'],
'grammar':[
'Which is a complete sentence?|The dog runs.|The dog.~Because the dog.~Running in the yard.|Type the action word in The dog runs.|runs|The complete sentence includes a subject and predicate.',
'Which word often signals a cause?|because|although~meanwhile~next|Type the conjunction in Because it rained, we stayed.|because|Because introduces a reason or cause.',
'Which sentence fixes the misplaced modifier?|Running to class, the student dropped a backpack.|Running to class, the backpack fell.~The backpack running dropped.~Running, a class was near a backpack.|Type the word for a describing word or phrase.|modifier|Place a modifier close to what it describes.',
'Which revision most clearly identifies the actor?|The committee revised the policy.|Revision of the policy was undertaken.~There was a revision.~Policy revision was in progress.|Type the term for changing a verb into a noun.|nominalization|Explicit agents and verbs often make prose easier to interpret.'],
'fiction':[
'Who is a character in a story?|a person who acts in the story|a page number~a table of contents~the book cover|Type the word for a person in a story.|character|A character is a participant in the imagined events.',
'What can reveal a character’s motive?|an important choice and its consequences|only the font size~only page numbers~only the jacket color|Type the word for a reason behind an action.|motive|Choices provide evidence about desires and values.',
'What should a reader consider about a narrator?|the limits of what the narrator knows|the publisher’s paper weight~the novel’s retail price~the number of margins|Type the term for the voice telling a story.|narrator|Viewpoint controls what information reaches the reader.',
'Which reading best handles an ambiguous ending?|compare multiple interpretations with evidence|announce one meaning without evidence~ignore contradictions~treat every reading as equal|Type the word for multiple plausible meanings.|ambiguity|A defensible interpretation explains specific details and alternatives.'],
'poetry':[
'What happens when a word repeats in a poem?|it can create rhythm|it changes into a number~it becomes silent~it removes meaning|Type the word for a pattern of beats.|rhythm|Repetition can create a perceived beat and emphasis.',
'Which phrase contains a metaphor?|The lantern was a small sun.|The lantern was metal.~The lantern sat outside.~The lantern was turned off.|Type the term for describing one thing as another.|metaphor|A metaphor invites a comparison without claiming literal identity.',
'What is subtext?|meaning implied but not stated directly|the printed title only~the final stage direction only~the exact word count|Type the term for implied meaning.|subtext|Pauses, gestures, and context can imply meaning.',
'How can a line break affect poetry?|by shifting emphasis and timing|by changing the ink’s color automatically~by proving a historical date~by removing the reader|Type the term for the arrangement of poetic lines.|lineation|Line breaks influence syntax, pauses, and emphasis.'],
'info':[
'What does germination mean?|a seed begins to grow|a leaf turns to glass~soil becomes a rock~a seed becomes a label|Type the word for the start of seed growth.|germination|Germination begins when conditions permit a seed to develop.',
'Which text feature helps explain a sequence?|arrows in a labeled diagram|an unlabeled decorative border~an unrelated advertisement~a blank page|Type the word for water moving over land.|runoff|Diagrams can clarify sequence, but their omissions matter.',
'What should be identified when evaluating a test?|its controlled and changing variables|only the club name~only a preferred answer~only a decorative title|Type the word for a changing feature in a study.|variable|Methods matter when comparing technical explanations.',
'What is a model in research?|a simplified representation for explanation or prediction|a perfect copy of all reality~an opinion that needs no evidence~a universal guarantee|Type the word for a simplified representation.|model|Models involve simplifications, assumptions, and limitations.'],
'evidence':[
'Which is an observation rather than a guess?|There are muddy footprints.|Mia made the prints.~A thief was there.~Everyone knows who walked there.|Type the word for information supporting an idea.|evidence|Seeing marks does not automatically identify their maker.',
'Which item is more directly checkable?|a dated lost-and-found entry|an unsupported hallway rumor~a guess about motives~an anonymous prediction|Type the word for a conclusion drawn from clues.|inference|Records can support a conclusion, but check what they actually record.',
'What does corroborating evidence do?|provides additional independent support|always proves every claim~removes the need for methods~changes opinions into facts|Type the verb meaning support with more evidence.|corroborate|Corroboration can strengthen confidence without guaranteeing truth.',
'What is a warrant in an argument?|reasoning that links evidence and a claim|an unrelated adjective~a citation style only~a final punctuation mark|Type the word for the bridge between evidence and claim.|warrant|Identify the inferential step instead of only listing facts.'],
'writing':[
'Which order makes a simple narrative clear?|beginning, middle, ending|ending, ending, ending~middle only~beginning only|Type the word for the order of events.|sequence|A narrative establishes what happened and in what order.',
'What is a useful purpose of revision?|to improve clarity and meaning|only to increase the word count~to remove every fact~to avoid considering the reader|Type the word for improving a draft.|revision|Substantive revision changes meaning and structure when needed.',
'Which organization often helps an explanation?|background before unfamiliar analysis|conclusion with no context~random unrelated details~repeated titles only|Type the word for logical connection across a text.|coherence|Organization should help the reader understand the reasoning.',
'Which change is substantive revision?|adding missing evidence and qualifying the thesis|changing one font color~adding a decorative border~renaming the file|Type the word for an essay’s central claim.|thesis|A revision should address the highest-impact weaknesses first.'],
'argument':[
'Which statement gives a preference and a reason?|I like this book because the pictures help me.|I like this book.~Book book book.~I have a book.|Type the word for an explanation supporting a preference.|reason|A because statement can connect a preference to a reason.',
'Which is an arguable claim?|The playground should add shade.|The sky exists.~A rectangle has four sides.~Two plus two is four.|Type the word for a supported position.|claim|A policy claim needs evidence, costs, and consideration of alternatives.',
'What is a counterargument?|a reason opposing the main claim|a repeated title~an unrelated joke~an unexplained statistic only|Type the word for an opposing argument.|counterargument|Represent objections fairly, then address their evidence.',
'Which combination is stronger persuasion?|a clear claim, relevant evidence, and an explained warrant|an emotional story alone~a chart without context~a slogan repeated many times|Type the word for strategic communication to an audience.|rhetoric|Persuasion should be assessed for logical, evidentiary, and ethical quality.'],
'research':[
'Which question can start an observation?|Why is this plant taller?|Is a plant?~Plant plant?~Green because?|Type the word for something asked to learn more.|question|An investigable question guides what to observe next.',
'What should be recorded when taking research notes?|where the information came from|only the page color~only a guess~only a smiley face|Type the word for an information origin.|source|Attribution allows a claim to be traced and checked.',
'What is provenance of an online image?|the documented origin and history of the image|its number of likes alone~its newest caption only~the viewer’s preferred story|Type the word for documented origin.|provenance|Context is essential when checking images and captions.',
'What should a good synthesis preserve?|meaningful differences in study methods|only the most convenient conclusion~the idea that every study is identical~only the author’s favorite quote|Type the term for integrating source findings.|synthesis|Synthesis compares evidence instead of silently flattening disagreement.'],
'speaking':[
'What shows active listening?|waiting and asking a relevant question|talking over the speaker~ignoring the speaker~changing the topic each time|Type the word for paying attention to a speaker.|listen|Active listening includes attention, understanding, and response.',
'What helps an audience read a chart?|clear labels and units|tiny unlabeled bars~unexplained abbreviations~a missing axis|Type the word for the people receiving a talk.|audience|Presentation details should serve the audience’s needs.',
'Which action tests whether you understood another speaker?|paraphrase their idea and ask if it is accurate|invent their position~change their words to a weaker claim~interrupt with a label|Type the word for restating meaning in new words.|paraphrase|Fair discussion checks understanding before criticism.',
'How should a research presenter discuss uncertainty?|show assumptions and properly labeled ranges|hide the method~report only the most dramatic number~claim all predictions are certain|Type the term for a stated limit on a claim.|qualification|Clear uncertainty communication supports responsible interpretation.']
}
assert all(len(records)==4 for records in SKILL_DRILLS.values())

def skill_drill(ident,band):
    row=SKILL_DRILLS[ident][band].split('|')
    assert len(row)==6,(ident,band,len(row))
    prompt,correct,distractors,fill_prompt,fill_answer,explanation=row
    distractors=distractors.split('~');assert len(distractors)==3
    return dict(prompt=prompt,correct=correct,distractors=distractors,fillPrompt=fill_prompt,fillAnswer=fill_answer,explanation=explanation)

def bucket(index):
    return 0 if index<=3 else 1 if index<=6 else 2 if index<=9 else 3

def parse_case(row):
    parts=row.split('|')
    assert len(parts)==12, (len(parts), row)
    return dict(zip(['title','actor','setting','action','observation','cause','result','limitation','next','word','definition','claim'],parts))

def first_keyword(phrase):
    stops={'a','the','an','in','of','and','with','to','by','from','that','was','were','who','for','its','this','their','how','why','what','does','at','on','as','may','can','could','did','not','some','each','after','about','which','into','rather','than','had','she','he','they','there','also','one','before','because','would','more','both','other','same','only'}
    words=[w.lower() for w in re.findall(r"[a-zA-Z]+",phrase) if len(w)>3 and w.lower() not in stops]
    return words[:3] or [phrase.lower()]

def make_passage(c,skill,stage,level):
    if stage==0:
        s=f"{c['actor']} was at the {c['setting']}. {c['actor']} {c['action']}. {c['observation'].capitalize()}. {c['result'].capitalize()}."
        if level!='PK': s+=f" We can learn that {c['claim']}."
    elif stage==1:
        s=(f"At the {c['setting']}, {c['actor']} {c['action']}. {c['observation'].capitalize()}. "
           f"This happened partly because {c['cause']}. {c['result'].capitalize()}. "
           f"The class noticed that {c['claim']}. One question remained: {c['limitation']}. "
           f"Their next step was to {c['next']}.")
    elif stage==2:
        s=(f"In the {c['setting']}, {c['actor']} {c['action']}. {c['observation'].capitalize()}. "
           f"The explanation matters: {c['cause']}. {c['result'].capitalize()}. "
           f"The passage advances a central principle: {c['claim']}. Yet the evidence has a boundary: "
           f"{c['limitation']}. Consequently, the group planned to {c['next']}. "
           f"The reader should distinguish the reported observation from the interpretation offered to explain it.")
    else:
        s=(f"During a project at the {c['setting']}, {c['actor']} {c['action']}. "
           f"The central observation was that {c['observation']}. This finding is important because {c['cause']}. "
           f"The immediate outcome was clear: {c['result']}. The broader claim is more qualified: {c['claim']}. "
           f"A critical reader should also consider the limitation: {c['limitation']}. "
           f"The next inquiry should be designed to {c['next']}. "
           f"Notice the distinction between an observation, a proposed explanation, a justified conclusion, and what remains unknown. "
           f"In academic discussion, these distinctions help prevent plausible interpretations from being presented as settled facts.")
    if level in ['C1','C2']:
        s+=(f" An academic response to this case should make its terms explicit, evaluate the relevance of the available evidence, "
            f"and explain how the conclusion might change if a competing interpretation were better supported. "
            f"When studying {skill.lower()}, avoid turning a descriptive pattern into a universal law without additional evidence. "
            f"A responsible analysis will present both the claim and its scope, then propose a feasible way to investigate the unresolved question.")
    return s


def add_question(qs,type_,prompt,**kw):
    qs.append(dict(id=f'q{len(qs)+1:02}',type=type_,prompt=prompt,points=10,**kw))

def objective_questions(c,skill,stage,level,guide,other,drill):
    qs=[]
    def mc(prompt,correct,distractors,rationale):
        opts=[correct]+distractors
        # rotate without randomness; different positional keys across lessons
        shift=(len(c['title'])+len(skill)+len(qs)+stage)%4
        opts=opts[shift:]+opts[:shift]
        add_question(qs,'mcq',prompt,options=[{'id':f'o{i}','text':x} for i,x in enumerate(opts)],answer=f'o{opts.index(correct)}',explanation=rationale)
    mc('What did the main person do in this reading?' if level in ('PK','K','1','2') else 'Which action does the reading explicitly describe?',
       c['action'],[x['action'] for x in other],
       'Return to the sentence describing what the person actually did. Evidence must come from the text.')
    mc('What did the person notice?' if level in ('PK','K','1','2') else 'Which observation is reported?',c['observation'],
       [x['observation'] for x in other],
       'The observation is a reported detail; it is not the broadest possible conclusion.')
    mc('What happened next?' if level in ('PK','K','1','2') else 'What outcome followed the work?',c['result'],
       [x['result'] for x in other],
       'The outcome appears in the passage and should not be exaggerated.')
    mc(drill['prompt'],drill['correct'],drill['distractors'],drill['explanation'])
    add_question(qs,'fill',f"Type the vocabulary word meaning: {c['definition']}.",answer=c['word'],alternatives=[],explanation=f"{c['word'].capitalize()} means {c['definition']}.")
    add_question(qs,'fill',drill['fillPrompt'],answer=drill['fillAnswer'],alternatives=[],explanation=drill['explanation'])
    causal_terms=first_keyword(c['cause'])[:2]
    outcome_terms=first_keyword(c['result'])[:2]
    add_question(qs,'short','Explain why the observation matters. Refer to the explanation in the reading.',
         keywords=causal_terms,minimumWords=5 if stage<=1 else 12,
         sample=f"It matters because {c['cause']}.",
         explanation='For a strong response, explain a causal or interpretive connection, not just repeat the outcome.')
    add_question(qs,'short','State a reasonable conclusion, and identify one limitation of this text.',
         keywords=first_keyword(c['limitation'])[:2]+first_keyword(c['claim'])[:1],minimumWords=7 if stage<=1 else 16,
         sample=f"A reasonable conclusion is that {c['claim']}. However, {c['limitation']}.",
         explanation='Distinguish an evidence-supported conclusion from an absolute claim.')
    steps=[c['action'],c['observation'],c['result']]
    add_question(qs,'order','Put the events in the sequence presented in the reading.',steps=steps,answer=[0,1,2],
         explanation='The text presents an action, the observation, and then the outcome. Other interpretations may come afterward.')
    minwords={'PK':6,'K':8,'1':15,'2':22,'3':35,'4':45,'5':55,'6':70,'7':85,'8':100,'9':120,'10':140,'11':165,'12':185,'C1':230,'C2':280}[level]
    if stage==0:
        prompt=f"Tell the story of {c['actor']} in your own words. Say what happened and why it was important. You can ask an adult to type your words."
    elif stage==1:
        prompt=f"Write a short response explaining what {c['actor']} learned. Include a detail from the passage and describe what should happen next."
    elif stage==2:
        prompt=f"Write an evidence-based response explaining how the case illustrates {skill.lower()}. Quote or paraphrase one detail, explain its relevance, and acknowledge a limitation."
    else:
        prompt=f"Write a nuanced analysis connecting the case to {skill.lower()}. Form a defensible claim, closely analyze specific textual evidence, consider an alternative interpretation, and propose a next inquiry."
    add_question(qs,'essay',prompt,minimumWords=minwords,
         keywords=(first_keyword(c['claim'])[:2]+first_keyword(c['observation'])[:1]+first_keyword(c['limitation'])[:1]),
         rubric=['Clear and relevant central idea','Accurate use of case details and interpretation','Organization and development','Sentence clarity and conventions'],
         sample=f"One defensible view is that {c['claim']}. The text reports that {c['observation']}. This matters because {c['cause']}. Still, {c['limitation']}. A useful next step would be to {c['next']}.",
         explanation='Extended writing receives only a provisional, local structural-and-keyword score. A human reader should evaluate accuracy, voice, insight, and fair treatment of evidence.')
    assert len(qs)==10
    return qs

def main():
    lessons=[]
    levels=[]
    strands=[{'id':ident,'name':name,'icon':icon,'description':desc} for ident,name,icon,desc in STRANDS]
    for i,(lid,label,stage,minwords) in enumerate(LEVELS):
        levels.append({'id':lid,'name':label,'stage':stage,'minimumExtendedWords':minwords})
        for j,(ident,name,icon,description) in enumerate(STRANDS):
            c=parse_case(CASE_ROWS[ident][bucket(i)])
            focus=SKILLS[ident][i]
            definition,example,strategy=GUIDES[ident]
            intro=(f"Today we will learn to {focus[0].lower()+focus[1:]}. Read the example with a helper, say your answer aloud, and try the questions. "
                   f"Take your time. You can ask a grown-up to type a response for you.") if i<=1 else (f"Learn to {focus[0].lower()+focus[1:]}. {example} "
                   f"Practice: {strategy}") if i<=3 else (f"This lesson focuses on how to {focus[0].lower()+focus[1:]}. "
                   f"{definition} Worked example: {example} Strategy: {strategy}")
            p=make_passage(c,focus,bucket(i),lid)
            others=[parse_case(CASE_ROWS[STRANDS[(j+k)%len(STRANDS)][0]][bucket(i)]) for k in (1,4,7)]
            qs=objective_questions(c,focus,bucket(i),lid,definition,others,skill_drill(ident,bucket(i)))
            lessons.append({'id':f'{lid.lower()}-{ident}','level':lid,'strand':ident,'index':j+1,
                            'title':focus,'readingTitle':c['title'],'objective':f"Learners will {focus[0].lower()+focus[1:]}.",
                            'instruction':intro,'steps':["Preview the learning target and worked example.","Read or listen to the original passage; note what is observed and what is inferred.","Answer the practice tasks. Check explanations and revise responses.","Submit all ten tasks to see a lesson score and targeted feedback."],
                            'passage':p,'glossary':[{'term':c['word'],'definition':c['definition']},{'term':'evidence','definition':'information used to support a conclusion'}],
                            'questions':qs,'estimatedMinutes':10 if i<=1 else 15 if i<=6 else 20 if i<=9 else 30 if i<=13 else 45,
                            'tags':[name,stage,focus]})
    content={'metadata':{'name':'ATLAS English Academy','version':'1.0','edition':'Preschool to College — Interactive Curriculum',
                         'description':'Original instructional mini-lessons, reading passages, and graded exercises for 16 learning levels.',
                         'lessonCount':len(lessons),'assignmentCount':sum(len(v['questions']) for v in lessons),
                         'scoreNote':'Objective items automatically scored. Short responses and writing receive provisional, explainable keyword/structure estimates, not semantic judgment.'},
             'levels':levels,'strands':strands,'lessons':lessons,
             'sources':[{'title':'Common Core State Standards — ELA','url':'https://corestandards.org/english-language-arts-standards/'},
                        {'title':'NICHD — National Reading Panel','url':'https://www.nichd.nih.gov/health/topics/reading/conditioninfo/Pages/teach.aspx'},
                        {'title':'Purdue OWL — Academic Writing','url':'https://owl.purdue.edu/owl/general_writing/academic_writing/index.html'}]}
    target=ROOT/'data.js'
    target.write_text('/* Original educational content. Rebuild using python build_content.py. */\nwindow.ATLAS_CONTENT = '+json.dumps(content,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    (ROOT/'curriculum.json').write_text(json.dumps(content,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Generated',len(lessons),'lessons and',content['metadata']['assignmentCount'],'assignments; bytes:',target.stat().st_size)
    print('Minimum passages',min(len(l['passage'].split()) for l in lessons),'maximum',max(len(l['passage'].split()) for l in lessons))

if __name__=='__main__': main()
