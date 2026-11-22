#!/usr/bin/env python3
"""ATLAS Reading Pathway v4. Original hypothetical case-based texts; no external content.
The instructional corpus is generated from a curated collection of 64 distinct scenario specifications.
"""
from __future__ import annotations
import json, re, hashlib, csv, os, textwrap, random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'source'
OUT=SRC/'pathway-v4'/'content'
OUT.mkdir(parents=True,exist_ok=True)
LEVELS=[('PK','Preschool',0),('K','Kindergarten',1)]+[(str(i),f'Grade {i}',i+1) for i in range(1,13)]+[('C1','College I',14),('C2','College II',15)]
# Eight knowledge domains with eight fictional case records each. All supplied figures and records are illustrative, not real research.
# Fields: topic | location | investigators | central question | observation A | observation B | hypothesis | intervention | competing explanation | limitation | focal term | definition | quantitative signal | reflective implication
RAW={
'Ecology':"""
Creek After a Storm|Willowbend Creek|a student water-testing team|whether rain changed creek clarity|the downstream sample looked cloudier than the upstream sample|a footpath drained into the same bend|stormwater carried loose soil into the creek|the class proposed a planted buffer beside the path|an old pipe may also have carried sediment|samples were collected on only two afternoons|sediment|small particles carried in water|clarity readings shifted from 18 to 11 units|a single reading should not settle a public decision
The Schoolyard Trees|Hollowbrook School|the school garden council|which courtyard spaces needed shade|the east pavement grew warmer after lunch|new trees already shaded the library wall|additional canopy could cool exposed gathering places|volunteers mapped potential planting sites|building shadows may have shaped the temperature pattern|the thermometers were used at different moments|canopy|the upper layer made by tree branches and leaves|the sunny surface measured 34 degrees and the shaded patch 27|careful comparisons need similar conditions
The Returning Bees|Cloverfield Garden|a neighborhood pollinator group|why fewer bees visited the garden in spring|the garden contained fewer early flowers|nearby yards used more ornamental stone|lack of blooming food could reduce visits|gardeners planned sequential flowering beds|cold weather could explain some of the decline|counts were made during a single week|pollinator|an animal that transfers pollen between flowers|visits averaged 9 per hour versus 15 in the prior log|one cause may not explain every change
Wetland Walkway|Marshlight Preserve|a trail committee|how to protect habitat while keeping a path open|wet ground showed new footprints beyond the boardwalk|birds nested close to the narrow trail|unmarked exits were disturbing sensitive ground|the committee proposed rails and interpretive signs|seasonal flooding also moved soil and plants|the bird survey covered a limited area|habitat|the surroundings an organism needs to live|trail departures were logged 22 times in three days|public access and protection can be balanced
The Compost Trial|Pinegate Orchard|a community garden class|whether compost improved soil water retention|one planter stayed damp after a dry morning|another planter crusted along the surface|organic matter might hold moisture longer|the group mixed finished compost into matched plots|different sun exposure could affect the comparison|the plots began with unequal soil texture|retention|the ability to keep something rather than lose it|moisture was 24 percent in one plot and 16 in another|a fair test begins with comparable groups
City Night Sounds|Lantern District|an urban ecology club|what made a street noisy at night|traffic peaks aligned with the loudest readings|a loading dock added occasional sharp sounds|vehicle flow might explain most of the noise|students recommended timed traffic counts|wind and microphone placement could change measurements|only one monitoring station was available|baseline|a starting measurement used for comparison|readings ranged from 48 to 71 decibels|measurement tools shape the story data seem to tell
The Fox Crossing|Briar Ridge|a wildlife observation circle|why animals crossed the road at one bend|tracks clustered beside a broken fence|a culvert carried water under the road|animals may be following the protected drainage corridor|the group suggested a marked wildlife passage|the tracks might include several different animals|no cameras verified the species|corridor|a connected route between places|19 track sets were mapped near one crossing|patterns can guide questions without proving causes
A Garden in Heat|Southgate Apartments|a tenants' climate team|which places offered relief on hot afternoons|dark benches felt hotter than light benches|the courtyard lacked a reliable drinking fountain|surfaces and shade shaped comfort during heat|residents proposed trees and covered seating|wind and building orientation also affected comfort|surface temperatures do not measure human health outcomes|exposure|contact with a condition or influence|bench surfaces differed by 12 degrees|community improvements need more than one measure
""",
'History':"""
The Missing Library Page|Ashford Library|a local history seminar|why a town ledger had an empty month|a torn binding appeared beside the missing pages|newspaper reports continued during the same month|the absence may reflect damage rather than silence|students compared copies in neighboring archives|the record keeper may never have entered those events|no complete duplicate of the ledger survives|archive|a place or collection preserving historical records|three notices referenced dates absent from the ledger|missing evidence must not be treated as proof nothing happened
A Bridge Remembered|Mapleford Bridge|the oral history club|why residents disagreed about a bridge opening|a photograph showed the bridge under construction|one interview recalled a public ceremony earlier|planning and opening events may have been confused|the club constructed a timeline of dated records|the photograph might have been mislabeled|some interview accounts were recorded decades later|chronology|the order in which events occurred|the two claimed dates differed by 14 months|memory and documentary evidence can inform each other
The Market Street Letter|Port Alder|a historical correspondence group|what caused a shopkeeper to relocate|a letter mentioned a new railway station|rent receipts rose in the same season|transportation access and costs both influenced the decision|students annotated the writer's reasons|family responsibilities might have mattered more|only one side of the correspondence survives|primary source|a record created close to the event being studied|rent increased by 8 coins in the surviving receipts|an individual's words need context
Two Newspaper Reports|Ferncross Town|a media history class|why two newspapers framed one meeting differently|one article emphasized a packed room|the other emphasized an early departure|the editors selected details to support different themes|the class compared headlines and omitted facts|reporters may simply have arrived at different times|neither article preserves the full meeting transcript|framing|the selection and emphasis of information|both accounts mention the same vote of 17 to 9|different narratives can contain shared evidence
Maps of a Changing Harbor|Seabridge Port|a cartography workshop|what the harbor maps reveal about trade|an older map labeled a public dock|a later map showed warehouses by the shore|changing trade patterns may have reshaped land use|students layered maps and marked uncertainty|a change in cartographic scale could distort comparisons|mapmaking conventions differed by century|scale|the relationship between map distance and real distance|warehouse symbols grew from 2 to 7|maps are authored documents rather than perfect mirrors
The Pottery Fragments|Stonewell Field|an archaeology learning team|what broken pottery could tell about daily life|fragments clustered near the hearth remains|some pieces carried repair marks|pots were used and maintained over time|students cataloged context before proposing interpretations|the fragments could have been moved by later digging|the excavation covered only one test square|context|the position and associations of an archaeological find|27 sherds came from a single layer|objects alone rarely identify the people who used them
The Assembly Petition|Riverhall|a civics history course|what petitioners wanted from the council|the petition asked for safer street lighting|a council note listed cost concerns|safety goals competed with budget limits|students compared the petition with meeting minutes|some residents might have opposed added lighting|the surviving petition lists only supporters|petition|a written request made to an authority|46 names appeared on the document|participation records do not show the opinion of everyone
Tracing a Family Route|Elmport Station|a migration history class|why a family traveled through several cities|a ticket stub named an intermediate stop|a letter described searching for work|employment opportunities may have influenced the route|the class combined dates and places into a cautious account|family connections could also have directed travel|few letters from the journey remain|inference|a conclusion drawn from evidence and reasoning|the surviving route lists four separate stops|interpretations should show what is known and unknown
""",
'Engineering':"""
The Paper Water Filter|Bluebird Workshop|an engineering design group|which filter materials removed visible particles|sand trapped larger particles in a jar test|cloth slowed water without clearing it as much|different layers could improve visible clarity|the team tested a layered filter prototype|clear water does not necessarily mean safe drinking water|the test did not measure microbes or dissolved substances|prototype|an early model built to test a design|flow time rose from 32 to 51 seconds|performance needs more than one criterion
Sunlight at the Bus Stop|Westmere Transit|a transportation design class|how to make waiting areas more comfortable|people stood beyond the existing shelter at noon|the shaded space moved across the sidewalk|shelter orientation affected useful shade|students modeled a wider canopy|a larger roof might obstruct pedestrian movement|the model used only summer sun angles|constraint|a limit that shapes what a design can do|the proposed roof covered 6 more square meters|good design weighs competing needs
The Wooden Span|Brookstone Park|a model bridge team|why two bridge models carried different loads|the truss model bent less under a textbook|the flat beam model used fewer pieces|the shape of supports changed load distribution|the team revised joints before another test|the glue strength differed among models|the loads were placed by hand|load|a force or weight supported by a structure|the truss held 12 books and the beam held 7|a fair comparison requires consistent assembly
Bicycle Lane Signals|Eastline Avenue|a street safety task force|why cyclists hesitated at a junction|turning cars crossed the proposed bike route|the current signal had no separate cycle phase|a protected signal interval might reduce conflicts|designers drafted a timed intersection sequence|longer cycle phases could delay other traffic|observations were made only during morning commutes|conflict point|a place where movement paths could collide|nine close interactions were logged in one hour|safer systems must account for everyone affected
Flood Warning Board|Canalview Road|a student sensor laboratory|whether water-level signs gave enough warning|a painted ruler was difficult to read in rain|residents relied on memory of past floods|a bright reference marker could improve decisions|the class designed a visible height gauge|false alarms might reduce trust in the system|the device was tested indoors rather than in a flood|threshold|a point at which a condition triggers a response|a test alarm activated at 23 centimeters|warning systems need reliability and clear communication
The Quiet Classroom|Silverleaf School|an acoustics design club|which surfaces reduced distracting echoes|hard walls reflected clapping sounds|soft panels reduced the decay time|some materials absorb sound energy|the club placed removable panels along one wall|the room also changed when furniture moved|the test used a phone microphone rather than calibrated gear|reverberation|the persistence of sound after its source stops|echo decay changed from 1.5 to 0.9 seconds|measurement quality limits the strength of conclusions
Heat in a Lunch Box|Redwood Cafeteria|a materials science class|which insulation kept a meal warm|the metal box cooled more quickly at the edges|the fabric sleeve held warmth longer|insulation slowed the transfer of thermal energy|students compared containers with equal starting temperatures|lid openings could explain part of the difference|thermometer readings had a small delay|insulation|material that reduces the transfer of heat|one container lost 8 degrees and another lost 13|design testing must isolate changing variables
Wind Against the Tower|Cedarport Lab|a student architecture team|which base made a model tower stable|a narrow base tipped under the fan|a wider base resisted the same airflow|lower centers of mass improve stability|the group redesigned the support footprint|heavier materials might also change performance|the fan speed varied slightly between trials|stability|resistance to falling or losing balance|the wider model lasted 44 seconds longer|one successful trial does not establish general reliability
""",
'Community':"""
The Shared Garden Plot|Rosefield Commons|a community garden committee|who should receive limited planting space|families requested plots of several sizes|some neighbors had no outdoor space at home|transparent allocation rules could improve access|the committee proposed a rotating lottery|experienced gardeners feared losing established plots|the survey reached only current volunteers|equity|fair treatment that accounts for different needs|requests exceeded available plots by 18|fair rules need public reasons
The Lunch Line Survey|Harborview School|a student council|why the lunch line moved slowly|the line paused at a single payment station|students spent longer choosing unfamiliar meals|layout and information might both affect delay|the council suggested clearer menus and two pickup paths|more staff might solve the problem differently|observations covered three lunch periods|bottleneck|a point that limits the flow of a process|the average wait was 14 minutes|solutions should target causes rather than symptoms
The Park Bench Debate|Orchard Lane Park|a neighborhood planning group|where new benches should be placed|older residents wanted seats near the entrance|young athletes preferred seats beside the field|different users valued different locations|the group proposed two small seating zones|maintenance budgets might permit only one zone|the feedback form was available only online|stakeholder|a person or group affected by a decision|58 of 90 replies named the entrance|majority preference does not erase minority needs
The Recycling Signs|Bayside Center|a volunteer education team|why people put paper in the wrong bin|signs used similar colors for different materials|some labels contained unfamiliar words|clear illustrations could reduce confusion|volunteers tested picture-based signs|bin placement could matter more than the signs|the trial lasted only four days|classification|sorting items into defined categories|sorting errors fell from 31 to 19 in a trial|apparent improvements need repeated checks
A New Bus Route|Northgate Station|a transit advisory panel|whether a proposed stop served more riders|the proposed location was near apartments|the old stop was close to a medical clinic|a small route change helped some groups and harmed others|planners compared walking paths and boarding counts|future construction could change demand|the rider counts excluded weekends|trade-off|a gain that requires giving up something else|the move saved 5 minutes for one group and added 7 for another|public choices contain distributional consequences
The Tutoring Circle|Millwood Library|an after-school volunteer group|which tutoring schedule worked for families|weekday sessions were crowded|Saturday sessions attracted different families|multiple schedules could widen participation|volunteers created a rotating calendar|different tutors might affect attendance|the records covered only one month|participation|taking part in an activity or decision|attendance rose from 21 to 29 per session|attendance is one measure of program success
The Mural Proposal|Crosswalk Square|a youth arts council|how to choose a design for a public wall|one design celebrated local workers|another emphasized river wildlife|public art can represent several kinds of community identity|artists proposed a shared composition|the mixed design might satisfy neither group fully|not every resident attended the workshop|representation|the way a work depicts people or ideas|36 people voted for the first design and 33 for the second|close votes invite more discussion
The Emergency Kit Shelf|Southbend Center|a mutual-aid planning team|what supplies a storm kit should contain|families asked for flashlights and batteries|some residents needed printed information in several languages|a useful kit depends on local needs|the group sorted supplies into labeled bins|limited storage made some donations impractical|the trial ignored people unable to visit the center|accessibility|the ease with which people can use something|the shelf held 84 kits at launch|a useful program must reach those with barriers
""",
'Technology':"""
The School App Permission|Summit Academy|a student privacy board|whether an app requested too much information|the app asked for contact-list access|its stated purpose was recording reading practice|some permissions were unrelated to the task|students drafted a minimal-permission checklist|the developer might use contacts for an optional feature|the group did not examine the app's source code|minimization|collecting only information needed for a purpose|four of seven permissions lacked a clear explanation|privacy questions begin with purpose and necessity
Search Result Order|Orion Library|a digital literacy team|why one search result appeared first|the first link was a sponsored listing|a later result contained more primary-source details|ranking can reflect payment as well as relevance|the team created a comparison checklist|the first page could still be reliable|the team tested only two search queries|ranking|the order in which a system presents results|three of five top results were advertisements|prominence should not be mistaken for quality
The Image Caption|Maple Tech Lab|an accessibility design club|whether images were understandable without sight|some diagrams had no text alternatives|a screen reader announced only file names|descriptive captions can preserve critical meaning|students wrote concise alternative text for each diagram|complex charts may need a longer text table|only one assistive technology was tested|alternative text|a text description used when an image is unavailable|captions were added to 18 of 20 diagrams|accessibility requires testing with actual users
Sensors in the Garden|Greenrise School|a coding and science team|why automatic watering sometimes ran in the rain|the sensor sat under a covered roof|the soil beside it was much drier than the open bed|an unrepresentative sensor location misled the controller|the team moved the probe and logged results|a software threshold might also have been wrong|the test period included little rainfall|sampling bias|error from observing an unrepresentative portion|watering activated six times during wet days|automation inherits limits of its input data
The Rumor Screenshot|Harborline Newsroom|a student fact-checking desk|whether a circulating screenshot was authentic|the screenshot cut off the publication date|the original webpage had a different headline|the cropped image changed the context of the report|students searched for the primary page|the screenshot might have come from an earlier edit|the original author's revision history was unavailable|provenance|the record of where information originated|the shared crop omitted 42 percent of the page|context can change the meaning of accurate words
The Lost Draft|Cypress Media Club|a school publishing team|why a project vanished after a computer restart|the file existed only on one device|automatic backups had been disabled|single-copy work is vulnerable to device failure|the class designed a versioned backup plan|a corrupt file could have caused the loss|the cause was not established by forensic analysis|redundancy|having additional independent copies|the group added two separate backup locations|resilience improves when failures are anticipated
The Fairness Dashboard|Northstar Lab|a data ethics seminar|whether an automated decision treated groups comparably|approval rates differed among two groups|the groups had different sample sizes|a headline percentage alone cannot identify unfairness|the seminar requested error-rate and context measures|unmeasured circumstances might affect outcomes|some input data were missing|disparity|a measurable difference between groups|rates were 61 percent and 74 percent in a sample|ethical claims need context and careful measurement
The Editable History Page|Unionfield Archive|a web literacy class|how an encyclopedia page changed over a week|an early version made a strong claim without citation|a later revision added two source links|revision history can reveal a changing evidence base|students compared snapshots rather than trusting one view|new links could still lead to weak sources|the class did not verify every cited document|revision history|a record of changes made to a document|seven edits appeared in the page log|transparent editing helps but does not guarantee truth
""",
'Literature':"""
The Lighthouse Notebook|Fogmere Point|Mira the apprentice keeper|whether a lost notebook could repair a friendship|Mira found a tide chart in her father's handwriting|her friend Noah waited outside the locked tower|an old promise had been misunderstood|Mira decided to read the notebook aloud|Noah believed silence was safer than another argument|the notebook did not describe the final conversation|subtext|meaning suggested rather than directly stated|the final page contained three unfinished sentences|readers infer feelings from action and omission
The Clockmaker's Door|Copperwick Lane|Lena the clockmaker|why a customer refused a finished clock|the customer pointed to a stopped second hand|Lena noticed a spring installed backward|pride had kept her from asking for help|she invited her former teacher to inspect the work|the customer may also have disliked the price|the story never reveals the customer's private thoughts|motivation|a reason a character acts|the repair required two careful adjustments|characters can change when they revise a belief
The Seed in Winter|Frostmill House|Amir the young gardener|what an unplanted seed came to represent|Amir saved one seed in a paper envelope|his sister planted hers before a late frost|waiting might reflect hope or fear|Amir finally planted the seed in a sheltered pot|his sister argued that action mattered more than waiting|the seed's later growth is not shown|symbol|an object that suggests an idea beyond itself|the envelope remained unopened for six weeks|one image can support more than one interpretation
The Unsent Postcard|Blueharbor|Jo the railway traveler|why a postcard stayed in a coat pocket|Jo wrote a greeting but crossed out the address|the station clock chimed as a train departed|Jo feared the reply more than the distance|Jo rewrote the message with a simple question|the missing address could have been accidental|the recipient never appears directly|narrator|the voice that tells a story|the postcard was rewritten twice|a narrator's knowledge may be limited
The Glass Violin|Meadowgate Theatre|Evelyn the young musician|why a beautiful violin remained silent|the instrument cracked in dry air|the orchestra continued rehearsal without her|Evelyn confused the damaged instrument with her own ability|she borrowed an ordinary violin and performed|the conductor valued persistence over perfection|the story offers no account of every audience member|theme|a central idea explored by a work|one final note rang after the lights dimmed|plot details gain significance through relationships
The Unmarked Path|Juniper Woods|Rosa and her cousin Eli|whether a shortcut was worth its uncertainty|a map showed a trail that ended at the creek|Eli claimed he knew an older route|confidence and knowledge are not the same|Rosa chose to follow the marked ridge path|Eli believed the creek route would save time|the older route was not actually tested|foreshadowing|a detail that hints at a later development|two broken signposts stood beside the trail|readers distinguish clues from certainty
A Window at Dawn|Bracken House|Tess the night baker|who had left bread outside the old door|the basket appeared before sunrise|a paper note thanked the town for its kindness|a quiet stranger might have been returning a favor|Tess placed her own loaf beside the basket|the note could have referred to another event|the author never names the visitor|ambiguity|uncertainty that allows several readings|four loaves were present by morning|stories can leave questions productively open
The Last Blue Ribbon|Crescent Fair|Daniel the young maker|whether winning justified breaking a promise|the model ship won the judges' praise|Daniel's teammate had built its damaged mast|Daniel had hidden his teammate's contribution|he corrected the record before accepting the ribbon|his teammate might still feel betrayed|the ending does not state whether trust fully returned|conflict|a struggle between competing goals or values|the judges made their decision in nine minutes|a story's ethical question may outlast its plot
""",
'Science':"""
Sleep and the Class Survey|Sunvale High|a classroom research group|whether sleep patterns related to concentration|students who reported more sleep also reported fewer distractions|the survey relied on self-reported times|sleep might be associated with attention|the group planned a better diary protocol|workload could affect both sleep and attention|the sample was small and nonrandom|correlation|an association between variables that does not prove causation|the sample contained 42 students|association is not a causal demonstration
Labels on the Cereal Box|Larkspur Market|a nutrition literacy class|why serving sizes confused shoppers|two boxes listed different serving masses|the front graphics showed similarly sized bowls|comparing equal weights would improve interpretation|students calculated values per 100 grams|ingredients and price also matter to a decision|some printed labels used rounded numbers|normalization|putting measures on a comparable scale|sugar values were 7 and 11 grams per listed serving|a fair comparison needs a shared denominator
The Cloud Chamber Log|Aster Observatory|a physics exploration class|why one observation appeared brighter|the room lights varied during trials|the instrument setting had also changed|brightness depended on more than one factor|students repeated observations at fixed settings|the phenomenon might have varied naturally|their equipment was not calibrated|variable|a characteristic that can take different values|the bright mark appeared in 8 of 20 trials|controlled settings support stronger inferences
The Medicine Study Headline|Crestview Journal|a science media workshop|whether a headline overstated a result|the headline declared a treatment a cure|the study summary reported a modest group difference|media language amplified limited evidence|students rewrote the headline with qualifiers|small effects can still matter in some contexts|the workshop saw only the abstract and not full data|qualifier|a word that limits or specifies a claim|the reported difference was 4 points on a 100-point scale|precise language respects uncertainty
The Lake Temperature Series|Mirrorwater Lake|a student field science team|whether the lake warmed over a month|afternoon readings were higher than morning ones|different days were sampled at different hours|time of day could confound the apparent trend|the group designed a fixed-hour schedule|a true seasonal trend might also exist|the series was incomplete|confounder|a factor linked to both a suspected cause and outcome|the 12 readings ranged from 14 to 21 degrees|data design matters before graphs are interpreted
The Soil Microbe Exhibit|Westbrook Museum|a biology exhibition team|how to explain unseen ecological processes|the model showed microbes breaking down leaves|visitors thought all microbes caused disease|a familiar example might correct the misconception|curators built a transparent decomposition model|the model could suggest an oversimplified ecosystem|the exhibit could not show microscopic diversity directly|decomposition|breaking down complex matter into simpler material|the display tracked five changes across three weeks|models clarify some aspects while hiding others
Two Test Groups|Bellmont Science Fair|a statistics learning group|whether two classroom strategies differed|one group improved on a short quiz|the groups started with different average scores|initial differences complicated the comparison|students used matched pretests in a follow-up|practice effects could improve either group|students were not randomly assigned|selection bias|distortion caused by how participants are chosen|the groups began at 62 and 74 percent|fair conclusions depend on group comparability
The Bird Count Map|Harper Marsh|a conservation science club|whether a mapped decline reflected fewer birds|new volunteers surveyed a smaller part of the marsh|an old count used a different observation route|effort differences might explain part of the decline|the team standardized observation hours and paths|migration timing could also shift counts|some species were difficult to identify|sampling effort|the amount of work used to collect observations|recorded species fell from 24 to 17|measurement changes can imitate real-world changes
""",
'Argument':"""
The School Budget Choice|Clearwater District|a student public-policy workshop|how to divide a limited improvement fund|science rooms needed new equipment|the library requested more accessible books|both proposals served important but different purposes|the class built a criteria-based budget matrix|some needs were not represented at the hearing|the total costs were preliminary estimates|opportunity cost|the value of the alternative not chosen|the proposed projects totaled 125 units against a budget of 100|budget decisions require explicit priorities
The Bicycle Repair Shop|Woodlane Market|a youth entrepreneurship club|whether a repair service could remain affordable|parts costs rose over the summer|more riders asked for low-cost tune-ups|demand could rise while profit margins shrank|the team considered tiered service prices|customers might choose another shop|the forecast relied on only six weeks of sales|margin|the difference between revenue and cost|a repair sold for 30 units with 19 units in direct costs|good business reasoning distinguishes revenue from profit
The Library Hours Proposal|Eastward Library|a civic writing seminar|whether the library should open later|students requested evening study space|staff reported higher weekend use|a small late-hour trial could test demand|the group proposed a four-week pilot|late opening increased staffing costs|one petition may not represent all patrons|pilot|a limited trial used to study a proposal|72 signatures supported later hours|proposals should specify what evidence would change a decision
The Reusable Cup Debate|Grandmill Campus|a sustainability policy club|whether a cup program reduced waste|single-use cup bins filled quickly|washing reusable cups consumed water and energy|a reuse system might help but required lifecycle thinking|students compared return rates and washing inputs|some users preferred the convenience of disposables|the program had no full environmental inventory|life cycle|the stages from production to disposal of a product|return rates reached 68 percent in the pilot|one visible waste stream is not the entire cost
The Local Product Claim|Ravenbrook Fair|a consumer research class|whether local labels justified higher prices|a banner promised community benefits|the product included imported components|local assembly and local sourcing are different claims|students proposed a transparent origin label|local wages might still be a meaningful benefit|supplier records were incomplete|transparency|clear disclosure of relevant information|only 3 of 8 components came from the district|precise definitions improve public debate
The Garden Water Rule|Linden Ridge|a neighborhood association|how to share water during a dry week|large gardens received more water under the old rule|new gardeners used smaller plots|a flat limit did not account for plot size|the association discussed measured allocations|meters would add cost and complexity|no data showed actual plant needs|allocation|the act of distributing a limited resource|one garden received 60 liters and another 20|fairness principles can conflict
Remote Learning Choice|Hillside School|an education debate class|when remote assignments helped learners|some students valued flexible schedules|others lacked quiet places to study|access conditions changed the usefulness of flexibility|the class proposed optional mixed delivery|multiple formats could increase teacher workload|the survey excluded several absent students|generalization|a conclusion extended beyond observed cases|29 of 50 respondents preferred mixed delivery|a sample's limits constrain the claim
The Repair or Replace Decision|Mason Hall|a facilities planning group|whether old desks should be repaired|the desks were sturdy but scratched|new desks would include adjustable heights|repair saved materials but might not meet accessibility needs|the group listed required features before pricing options|new products could have larger shipping impacts|the bids did not include long-term maintenance|criteria|the standards used to judge choices|repair cost 45 units and replacement 110 per desk|a choice should be evaluated against its goals
"""
}
FIELDS=['title','place','actor','question','evidence1','evidence2','hypothesis','intervention','alternative','limitation','term','definition','measurement','implication']
CASES=[]
for domain,body in RAW.items():
    lines=[x.strip() for x in body.splitlines() if x.strip()]
    assert len(lines)==8,(domain,len(lines))
    for line in lines:
        seg=line.split('|');assert len(seg)==len(FIELDS),(domain,len(seg),seg[0])
        rec=dict(zip(FIELDS,seg));rec['domain']=domain;CASES.append(rec)
assert len(CASES)==64
SKILLS=[
('Observation and detail','Identify a directly stated detail and distinguish it from an idea not stated.'),
('Sequence and cause','Trace the order of events without confusing sequence with causation.'),
('Context vocabulary','Infer the meaning of a word from its context, then check an explicit definition.'),
('Central idea','Identify the main claim and distinguish it from supporting details.'),
('Evidence and warrants','Explain how a piece of evidence does or does not support an interpretation.'),
('Perspective and purpose','Compare what two speakers choose to emphasize and why.'),
('Claims and limits','Locate the boundaries of what the available evidence can establish.'),
('Data literacy','Read quantities carefully and avoid comparisons with mismatched measures.'),
('Counterarguments','Represent a reasonable competing explanation before responding.'),
('Synthesis across texts','Connect two documents while preserving differences and uncertainty.'),
('Rhetoric and framing','Identify audience, tone, selection, and the work of qualifiers.'),
('Transfer and critique','Apply an analytical strategy to unfamiliar evidence.'),
]
GENRES=['narrative','investigation','memo','interview','editorial','case study','field notes','comparative report']
GRADE_TARGET={
'PK':(45,2),'K':(75,3),'1':(100,4),'2':(140,5),'3':(190,6),'4':(250,7),'5':(310,8),'6':(390,9),'7':(460,10),'8':(535,11),'9':(615,12),'10':(680,13),'11':(730,14),'12':(780,15),'C1':(940,18),'C2':(1060,20)
}
# Guide clauses are genuine explanations connected to each scenario; short reading passages remain decodable for younger learners.

def seedpara(c,n,l):
    place,actor=c['place'],c['actor']
    base=[
 f"At {place}, {actor} started with a question: {c['question']}? A group discussion did not settle it. To understand the situation, the readers must decide what is observed, what is inferred, and what still needs to be checked. A confident voice is not a substitute for evidence.",
 f"The first observation was specific: {c['evidence1']}. The second observation added a complication: {c['evidence2']}. Both details belong in the record, even if they make a neat explanation more difficult. Careful readers should underline what a witness could see directly and circle the explanations people attached to those observations.",
 f"An initial interpretation was that {c['hypothesis']}. This idea mattered because it gave the inquiry a direction, but it was not a demonstrated fact. A hypothesis helps readers ask which prediction would follow if the idea were true. The strongest inquiry is one that could discover the hypothesis was mistaken.",
 f"A useful record also includes quantities. In this case, {c['measurement']}. Numbers may look precise while the conditions of measurement remain uncertain. Before comparing them, readers should ask whether the quantities refer to the same time, population, method, and unit. Precision in a number does not automatically create accuracy in a conclusion.",
 f"One word helped clarify the issue: {c['term']}. In this case, {c['term']} means {c['definition']}. That meaning is not decoration; it helps the reader know exactly which feature of the situation is being discussed. A reader should test the definition against the example rather than merely memorize the word.",
 f"The team suggested a next action: {c['intervention']}. That proposal connected the observed concern with something people might realistically change. A proposal is not a result. Its value depends on a reasonable explanation of how the action could affect the conditions and on a plan to notice whether the predicted improvement appears.",
 f"Another participant raised a different possibility: {c['alternative']}. This response did not erase the original explanation; it tested its exclusiveness. When different causes fit the same observation, a conclusion should remain provisional. Readers should not dismiss a counterargument merely because it makes the preferred conclusion less dramatic.",
 f"The record contained an important limitation: {c['limitation']}. This sentence changes how far the writer may go. Even if the main interpretation seems reasonable, a limitation can restrict which populations, dates, or causes the evidence concerns. Good academic prose often sounds cautious because it makes those restrictions explicit.",
 f"A short meeting at {place} revealed several priorities. Some people wanted quick action. Others wanted more measurements before allocating time and materials. The disagreement was not simply a contest between caring and indifference; it reflected different judgments about risk, delay, cost, and the reliability of the initial record.",
 f"Imagine that an editor replaced 'the observations suggest' with 'the observations prove.' The descriptive facts would not have changed, but the strength of the assertion would. Readers should notice such shifts in modality. Words including may, suggests, appears, and demonstrates mark different degrees of confidence, and those degrees must fit the evidence.",
 f"The case invites a narrower claim: the observations give a reason to investigate {c['question']}, but they do not establish every part of an explanation. That distinction matters whenever an author combines a narrative, a number, and a proposed response. Readers can acknowledge an urgent concern without pretending to know more than the records show.",
 f"To summarize the investigation responsibly, a student can use four clauses: the issue, the observed details, the most plausible explanation, and the strongest remaining uncertainty. Each clause plays a separate role. Omitting the uncertainty can produce an exaggerated conclusion, while omitting the evidence turns the summary into an unsupported opinion.",
 f"Suppose a new observer arrives with a different report. The correct response is not necessarily to discard all earlier reasoning. It is to compare methods, look for conflicting information, and revise confidence. Evidence-based thinking treats a conclusion as something that can improve when the underlying record improves.",
 f"The final lesson is practical: {c['implication']}. That statement expresses a principle, not a measurement. A strong reader can explain which details support the principle and where the example stops. The difference between a fact, an inference, and a recommendation remains essential from the first school years to college seminars.",
 f"A second reading might call the story a success because a concrete response was suggested. A third might call it unresolved because the results of that response are not yet known. Both interpretations need to say what they count as success. A careful critique compares evaluation criteria rather than relying only on an appealing ending.",
 f"If a class uses this case as a model for another topic, it should carry over the method, not the specific conclusion. Asking for a source, identifying a plausible rival explanation, and testing a measurement can work in many disciplines. The observed facts at {place}, however, are unique to this constructed situation.",
 f"Readers sometimes equate a story's vivid detail with the reliability of its claim. Vividness can support attention and memory, but the reliability of a claim depends on the origin of the detail, the process that recorded it, and the degree to which another person could check it. Notice how these standards differ from the appeal of an anecdote.",
 f"In the final comparison, weigh three considerations: how well the explanation accounts for {c['evidence1']}; whether it also accommodates {c['evidence2']}; and whether the stated limitation leaves open a substantially different explanation. The strongest conclusion is not always the most emphatic one. Often it is the one that specifies exactly what further evidence would change the judgment.",
 f"A college-level reading should separate the author's normative preference from the empirical claim. Preferring {c['intervention']} is a judgment about what should be done; claiming it will work is a prediction about what will happen. These propositions require different kinds of support and may deserve different levels of confidence.",
 f"Finally, consider the counterfactual question: if {c['alternative']}, what additional observation would help separate that possibility from the original hypothesis? Framing the problem this way turns the debate into a plan for learning. It does not make the answer easy, but it makes the reasoning visible to criticism.",
 ]
    return base[n%len(base)]

def accessible_para(c,grade,n):
 # For young readers, decodable short sentences with a coherent beginning, middle, and response.
 first=[
 f"At {c['place']}, people noticed a problem. They had a question to answer.",
 f"They saw this: {c['evidence1'].capitalize()}. They looked again.",
 f"They also saw this: {c['evidence2'].capitalize()}. The clues did not tell the whole story.",
 f"The team had an idea. They thought {c['hypothesis']}.",
 f"They had another plan. They said that {c['intervention']}.",
 f"One person had a different idea. They thought {c['alternative']}.",
 f"The group was careful. They knew that {c['limitation']}.",
 f"They learned to ask, 'What did we see? What do we still need to know?'",
 f"The word {c['term']} means {c['definition']}.",
 f"The team did not have every answer. They could learn more by checking again.",
 ]
 txt=first[n%len(first)]
 if grade<=1:
  # Shorten syntax for true emergent levels and reduce the number of unfamiliar proper nouns.
  core=[
   f"We read a story. It is called {c['title']}. We can look and ask.",
   f"We can look at {c['place']}. We can see a clue. A clue can help us.",
   f"We see a clue: {c['evidence1']}. A grown-up can help us read this line.",
   f"Now we can ask: What did we see? We can tell the story in our own words.",
   f"The group has an idea. We can check if it is right. We can learn.",
   f"We read, we look, and we ask. The story is about {c['title']}.",
  ]
  return core[n%len(core)]
 if grade==2:
  return re.sub(r'\bThe clues did not tell the whole story\.', 'The clues helped, but were not enough.',txt)
 return txt

def companion_para(c,n):
 chunks=[
 f"DOCUMENT B — A different voice. One member of the group begins with the same problem at {c['place']}, but argues that the first interpretation deserves more skepticism. The member accepts the report that {c['evidence1']}. Acceptance of an observation is not acceptance of a particular causal story about it.",
 f"The alternative claim is straightforward: {c['alternative']}. If that explanation is possible, then the initial hypothesis—{c['hypothesis']}—must be tested against it, not simply repeated. A fair comparison asks what each explanation would predict and what observation could discriminate between them.",
 f"A practical difficulty complicates that comparison: {c['limitation']}. The difficulty may affect the sample, the timing, the location, or the instrument. Without describing the limitation, a reader might incorrectly assume that the record covers a wider situation than the investigators actually observed.",
 f"Those who favor {c['intervention']} may have a reasonable concern about delay. Yet the merits of taking a precautionary step are separate from the claim that the step has been proven effective. A responsible decision can proceed under uncertainty if its reasons, costs, and evaluation plan are explicit.",
 f"The second document therefore recommends a limited trial instead of a definitive judgment. It uses the measurement—{c['measurement']}—as a starting point and asks that the next observations be collected using a consistent protocol. The purpose is not to win an argument, but to make the argument more answerable.",
 f"In the margin, identify two places where this account differs from Document A. One difference concerns the strength of a claim; another concerns what should happen next. Neither difference requires the documents to disagree about every observation. Comparisons become clearer when agreement and disagreement are recorded separately.",
 f"The word {c['term']} also matters here because it means {c['definition']}. One writer may use a technical word as a shorthand; a reader should unpack the exact meaning before accepting the conclusion. An argument can be persuasive in tone and still depend on an undefined term.",
 f"A final question remains: what new record would change the second writer's mind? A serious skeptical position specifies such a condition. Skepticism without a possible standard of revision becomes a refusal to learn, just as certainty without evidence becomes an assertion rather than a supported conclusion.",
 ]
 return chunks[n%len(chunks)]

def source_para(c,n):
 lines=[
 f"SOURCE DOSSIER — Constructed classroom record. Item A records that {c['evidence1']}. This is a direct observation in the fictional case, not an independently verified public record.",
 f"Item B records a second detail: {c['evidence2']}. The detail should be read alongside Item A because a single vivid fact can mislead when it is detached from the surrounding conditions.",
 f"Item C contains a quantitative report: {c['measurement']}. Its interpretation requires attention to units, sample size, measurement conditions, and whether the values are actually comparable.",
 f"Item D notes a limitation: {c['limitation']}. Any summary that omits this qualification risks overstating the force of the available information.",
 f"Item E records an inference that {c['hypothesis']}; Item F records the rival explanation that {c['alternative']}. Both are interpretations rather than direct observations, even when each can be made to sound plausible.",
 f"Item G records a proposed action: {c['intervention']}. The proposal needs an outcome measure and a comparison condition before it can be described as an established success.",
 f"An annotation prompt asks readers to label each item observation, claim, rival hypothesis, qualification, numerical evidence, or proposed response. The value of this classification is that it prevents evidence and interpretation from being flattened into one story.",
 f"For a short synthesis, name one observation shared by Documents A and B, identify the conclusion that differs, and specify the single most informative new piece of evidence. Then state the limits of your synthesis without adding facts the documents do not supply.",
 ]
 return lines[n%len(lines)]

# Additional long-form lectures are constructed in a curriculum-specific way, not padding strings.
LECTURE_PARTS=[
 ("Preview and predict", "Before reading, inspect the title and genre. Ask what the writer would need to establish for the central claim to be credible. A prediction is a question to check, not a conclusion to force onto the text."),
 ("Mark what the record says", "Underline statements that can be pointed to in the document. Avoid treating your own guess about a person's motives as a directly reported fact. Record the wording that led you to each inference."),
 ("Find the main question", "The guiding question is often narrower than the topic. Rewrite it as a question requiring a specific answer. Distinguish this from the background setting, which may be interesting but not decisive."),
 ("Read a number carefully", "Identify the measured thing, the scale, the group, and the conditions. Ask what is missing. A numeric comparison is not meaningful when the denominators or observation conditions differ."),
 ("Resolve unfamiliar words", "Use clues in the surrounding sentence, infer a possible meaning, and then check against the definition. The purpose is to recover the author's meaning, not to replace every unfamiliar word with a convenient guess."),
 ("Track the argument", "A useful argument map connects claim, evidence, warrant, qualifier, objection, and response. Some texts omit one or more elements; naming an omission can be an analytical observation if the missing element matters."),
 ("Distinguish cause and correlation", "An association, a temporal sequence, and an experiment are different kinds of evidence. A cause claim needs a plausible mechanism and consideration of alternative explanations; two values alone rarely establish it."),
 ("Hear other perspectives", "Summarize a competing claim in a way its supporter might recognize. A counterargument deserves an accurate statement before evaluation. Critiquing a caricature weakens your own reasoning."),
 ("Study the source", "Ask who produced the document, for which audience, under what constraints, and with access to what observations. A source can be authentic without being complete or unbiased."),
 ("Annotate limitations", "Underline phrases specifying sample, time, place, scope, and uncertainty. These are not merely weaknesses; they often demonstrate that the writer understands how much the evidence can justify."),
 ("Synthesize, do not merge", "When two documents agree on details but disagree on interpretation, preserve both the agreement and the disagreement. A synthesis should not invent a middle claim merely to make the accounts sound harmonious."),
 ("Revise your explanation", "Give a concise answer, include a relevant quotation or precise paraphrase, explain why it matters, and state a qualification. Revision should strengthen reasoning rather than only replace small words with impressive ones."),
]

def level_skill(grade):
 if grade <= 1: return 'Listen, point to words, name a detail, and retell a beginning and ending with an adult.'
 if grade <=3: return 'Retell accurately, identify a main idea, notice sequence, and quote a simple clue.'
 if grade<=5: return 'Summarize across paragraphs, distinguish evidence from opinion, and compare two simple accounts.'
 if grade<=8: return 'Trace an argument, identify a limitation, use quoted evidence, and test an inference against the text.'
 if grade<=12:return 'Evaluate source reliability, rhetorical purpose, quantitative claims, and rival interpretations across documents.'
 return 'Produce defensible close readings and syntheses, distinguish methodological and normative claims, and evaluate plausible counterarguments.'

def main_paragraphs(c, grade, order):
 # The first 8 entries are foundational for all stronger readers, followed by varied advanced analytical moves.
 if grade<=1:return [accessible_para(c,grade,i) for i in range(3 if grade==0 else 4)]
 if grade<=3:return [accessible_para(c,grade,i) for i in range(6+grade)]
 n=(10 if grade==4 else min(20,11+grade//2))
 # rotating paragraphs varies focus among grade levels and subjects while retaining crucial first 8 anchors
 return [seedpara(c,i,grade) for i in range(n)]

def companion_paragraphs(c,grade):
 if grade<=2:return [f"Another reader said, '{c['evidence1'].capitalize()}.' We can look for another clue.",f"We can ask if {c['hypothesis']}. A good reader asks a question."]
 if grade<=4:return [accessible_para(c,grade,i) for i in range(4,8)]
 return [companion_para(c,i) for i in range(5 if grade<=7 else 8)]

def source_paragraphs(c,grade):
 if grade<=1:return [f"Fact card: {c['evidence1'].capitalize()}.","Question: What did you read? Point to the words."]
 if grade<=5:return [f"Record A: {c['evidence1'].capitalize()}.",f"Record B: {c['evidence2'].capitalize()}.",f"An idea is different from a clue. The idea was that {c['hypothesis']}.",f"Number note: {c['measurement']}.",f"Word note: {c['term']} means {c['definition']}.",f"Limit note: {c['limitation']}."]
 return [source_para(c,i) for i in range(5 if grade<=8 else 8)]

def teacher_explanation(c,skill,grade,part):
 h,base=LECTURE_PARTS[part]
 obj=SKILLS[skill%len(SKILLS)]
 examples=[
 f"For example, the sentence '{c['evidence1']}.' reports one observation; the sentence '{c['hypothesis']}.' proposes an explanation.",
 f"In this case, the different observation '{c['evidence2']}' changes which questions deserve attention.",
 f"The limitation '{c['limitation']}' should appear in the final interpretation, even when it weakens an appealing claim.",
 f"A reader may test the proposal '{c['intervention']}' by specifying what outcome to observe before and afterward.",
 f"Do not forget the alternative: '{c['alternative']}'. A fair reading asks whether the available record rules it out.",
 f"The measure '{c['measurement']}' cannot be interpreted independently of how and when it was collected.",
 ]
 exercise=[
 "Try it: underline one exact observation and rewrite one inference beginning with 'This may suggest'.",
 "Try it: state one thing the text does not reveal, and explain why that missing detail matters.",
 "Try it: write a one-sentence central idea followed by a directly relevant detail.",
 "Try it: identify a word whose meaning depends on the passage and explain the nearby clues.",
 "Try it: identify the strongest counterclaim before you explain whether you agree.",
 "Try it: describe one new measurement or document that would change your conclusion.",
 ]
 return {"heading":h,"explanation":base,"workedExample":examples[part%len(examples)],"practice":exercise[part%len(exercise)],"learningTarget":obj[1],"levelGuidance":level_skill(grade)}

def make_questions(c, grade, module, levelid):
 # All closed-choice questions are factually derived from the passages and keyed to correct semantic alternatives.
 stem=c['evidence1'];other=c['evidence2'];lim=c['limitation'];hyp=c['hypothesis'];alt=c['alternative'];act=c['intervention'];
 g=grade
 if grade<=1:
  title=c['title']; place=c['place']; lead=title.split()[0].strip('.,')
  checks=[
   ('title','What is the title of our story?',title,['My Red Hat','The Little Cup','A Rainy Walk'],'Read the story title aloud, then find its exact words.'),
   ('word','Which word is in this sentence: "We can look and ask"?','look',['jump','blue','train'],'Point to the word in the sentence and say it aloud.'),
   ('letter','What is the first letter in the word "read"?','r',['b','t','s'],'The written word read starts with r.'),
   ('sounds','Which word begins with the same sound as "sun"?','sit',['map','dog','fun'],'Both sun and sit begin with the /s/ sound.'),
   ('rhyming','Which word rhymes with "see"?','bee',['hat','sit','dog'],'Listen for the final /ee/ sound.'),
   ('question','Which mark goes at the end of a question?','?',['.','!',','],'We use a question mark when writing a direct question.'),
   ('sentence','Which sentence begins with a capital letter and ends with a period?','We can read.',['we can read.','We can read','we can read'],'Sentences start with a capital letter and end with an appropriate mark.'),
   ('meaning','What can a clue help us do?','learn something',['forget everything','skip every word','change a fact'],'A clue provides information we can use.'),
   ('comprehension','What can we do after we read?','tell the story',['tear the book','skip all words','hide the page'],'Retelling helps show what we understand.'),
   ('thinking','If we are unsure, what should we do?','look again and ask',['guess and say we know','ignore the text','say the story is wrong'],'Good readers check the words and ask questions.'),
  ]
  out=[]
  for i,(kind,question,right,wrong,explain) in enumerate(checks):
   values=[right]+wrong;shift=(module+i+grade)%4;opts=values[-shift:]+values[:-shift] if shift else values
   out.append({'id':f'q{i+1:02}','kind':kind,'type':'mcq','question':question,'options':opts,'correct':opts.index(right),'explanation':explain,'evidence':right,'points':10})
  return out+[
   {'id':'r01','kind':'speaking','type':'writing','question':f'With an adult, tell one thing you notice in {title}.','model':'A child may point, draw, gesture, or speak. Support age-appropriate comprehension.','requiredEvidence':[],'rubric':['Notices one feature','Shares a response in their own way'],'points':0},
   {'id':'r02','kind':'phonics','type':'writing','question':'Write or say a word that begins with the same sound as sun.','model':'Examples include sit, sock, and sand.','requiredEvidence':[],'rubric':['Recognizes the starting /s/ sound'],'points':0},
   {'id':'r03','kind':'retell','type':'writing','question':f'Ask an adult to read {title}; then draw or tell the beginning and ending.','model':'Retelling is evaluated by a parent or teacher, not exact string matching.','requiredEvidence':[],'rubric':['Communicates in words, gestures or a drawing','Identifies one story detail'],'points':0}]
 specs=[
 ("explicit", "Which detail is directly reported in the reading?",stem,[hyp,alt,act],"A directly reported detail can be pointed to in the passage; proposed explanations and actions cannot replace it."),
 ("second-source", "Which additional observation appears in the case?",other,[hyp,alt,lim],"A second observation broadens the record and may complicate the first interpretation."),
 ("inference", "Which statement is an interpretation rather than a directly observed fact?",hyp,[stem,other,c['measurement']],"A hypothesis explains observations; it is not itself an observation."),
 ("limitations", "Which statement describes a limit on the available evidence?",lim,[act,other,stem],"A limitation identifies a reason to avoid extending a conclusion too far."),
 ("rival", "Which statement gives a plausible alternative explanation?",alt,[act,c['term']+' means '+c['definition'],stem],"A rival explanation fits some of the same observations but suggests another cause or interpretation."),
 ("proposal", "Which statement proposes an action rather than reporting a finding?",act,[lim,other,hyp],"Proposals say what someone wants to try; findings report what has been observed."),
 ("vocabulary", f"In this lesson, what does '{c['term']}' mean?",c['definition'],['a claim that cannot be questioned','a number without a unit','an action that has already succeeded'],"Use the explicit glossary definition, then verify its use in the passage."),
 ("measurement", "Which statement accurately repeats the recorded quantitative information?",c['measurement'],["the numbers demonstrate that the proposal worked","the figures represent a randomized clinical trial","the data prove all possible rival explanations wrong"],"Read the numerical claim exactly as provided; do not silently upgrade it into causal proof."),
 ("source-critical", "What is the fairest judgment about the case evidence?","The observations are relevant, but the stated limitation prevents a final causal conclusion.",["The first explanation is certainly correct.","No useful information is available.","The proposed action has already been validated."],"Evidence may be informative and incomplete at the same time."),
 ("transfer", "Which next step would most improve confidence in the proposed explanation?","Collect comparable new observations and test the rival explanation.",["Replace every qualifying word with 'proves'.","Repeat the original claim more forcefully.","Remove inconvenient observations from the report."],"A stronger investigation plans how to challenge its preferred interpretation."),
 ]
 # Domain-specialized transfer checks avoid treating every discipline as the same generic worksheet.
 domain_pairs={
  'Literature':[
   ('interpretation','How can readers support an interpretation of a character?', 'Connect particular actions and details to an idea while acknowledging ambiguity.', ['Assume the author revealed every private thought.','Choose the most exciting explanation without evidence.','Treat a symbol as having exactly one meaning.'],'Interpretations need textual evidence, and some stories intentionally leave uncertainty.'),
   ('literary-transfer','What is a responsible response to an unresolved ending?', 'Explain more than one plausible reading and identify the detail supporting each.', ['Invent a final event that is not in the story.','Say the author forgot to finish the story.','Ignore details that complicate the preferred ending.'],'An ambiguous ending supports disciplined interpretation rather than unsupported invention.')],
  'History':[
   ('historical-method','What is the best way to evaluate an incomplete historical record?', 'Compare surviving sources and identify what each source can and cannot establish.', ['Assume the missing pages prove nothing happened.','Use the oldest source without examining its purpose.','Merge all contradictory accounts into one certain story.'],'Historical inference depends on provenance, date, completeness and corroboration.'),
   ('historical-transfer','Which practice most improves a historical explanation?', 'Separate what a record directly reports from an inference about its cause.', ['Treat every memory as a literal transcript.','Discard an account whenever another differs.','Ignore the original context of an artifact.'],'Evidence and interpretation must remain distinguishable.')],
  'Engineering':[
   ('design-method','What would make a design comparison more reliable?', 'Test prototypes under matched conditions and measure the specified performance criteria.', ['Compare one prototype indoors and one outdoors.','Change several variables without tracking them.','Assume a beautiful prototype must work better.'],'Consistent test conditions make observed performance differences more meaningful.'),
   ('design-transfer','What should a designer do before calling a prototype successful?', 'Repeat tests, examine trade-offs and check whether the design meets its constraints.', ['Rely on one successful trial.','Ignore users whose needs differ.','Count the proposal as the measured outcome.'],'Performance, reliability and competing constraints belong in design evaluation.')],
  'Community':[
   ('civic-analysis','What should be included in a fair public recommendation?', 'Different groups’ needs, the practical constraints and evidence for the proposed change.', ['Only the preference of the loudest speaker.','A vote count with no attention to access barriers.','The easiest outcome without reasons.'],'Community decisions affect differently situated stakeholders.'),
   ('civic-transfer','How can readers tell a proposal from its demonstrated effect?', 'A proposal describes an action; its effect requires subsequent evidence.', ['An attractive poster proves a program worked.','A majority vote removes every trade-off.','A planned project is already an evaluated result.'],'A recommendation is not a record of measured outcomes.')],
  'Technology':[
   ('digital-critical','Which approach best evaluates a digital system claim?', 'Check the data’s origin, the measurement method and alternative explanations.', ['Trust the first search result because it is first.','Assume a dashboard shows every relevant condition.','Treat automated output as unbiased by definition.'],'Data provenance and system context matter.'),
   ('digital-transfer','What is a good safeguard when a digital result looks certain?', 'Look for missing cases, sampling limits and ways the result could be tested.', ['Hide the system’s limitations.','Replace an uncertainty label with guaranteed.','Accept numerical precision as proof of fairness.'],'Well-presented numbers can still reflect imperfect inputs or sampling.')],
  'Science':[
   ('science-critical','What conclusion is justified by an observational association?', 'The two measurements may be related, but other explanations still need examination.', ['One observation always proves a cause.','A precise instrument eliminates all confounding.','A sample necessarily describes every possible population.'],'Association and causal identification are different scientific claims.'),
   ('science-transfer','What would help distinguish a cause from a confounder?', 'Improve comparison conditions, record relevant variables and repeat observations.', ['Change the hypothesis after seeing each result without noting it.','Ignore unexpected data.','Use a headline as a substitute for a method section.'],'Good research design seeks explanations that survive plausible alternative accounts.')],
  'Argument':[
   ('argument-quality','What makes a policy argument stronger?', 'An explicit criterion, relevant evidence, a reasonable objection and a qualified recommendation.', ['Treat a preference as if it were measured fact.','Ignore costs borne by other people.','Declare there are no alternatives.'],'A strong argument shows its warrants, standards and trade-offs.'),
   ('argument-transfer','What should a critic evaluate before rejecting a proposal?', 'Whether its evidence supports the specific conclusion and how it addresses a counterargument.', ['Only whether the speaker sounds confident.','Whether the title is long and impressive.','Whether the recommendation is popular online.'],'An argument should be judged by support and reasoning, not only style.')],
  'Ecology':[
   ('ecology-critical','Which conclusion best respects a limited field observation?', 'A local pattern warrants further study, but should not automatically be generalized.', ['The pattern must be identical in every ecosystem.','One sample proves the proposed intervention worked.','A field limitation makes every observation useless.'],'Field observations are useful within the scope of their methods.'),
   ('ecology-transfer','What would strengthen an environmental field comparison?', 'Repeated sampling at comparable times and locations, including rival explanations.', ['Measure only after the preferred intervention.','Ignore changes in weather or observation effort.','Assume every location has identical conditions.'],'Environmental change and measurement change need to be distinguished.')],
 }
 specials=domain_pairs[c['domain']]
 specs[-2:]=specials
 out=[]
 for i,(kind,question,right,wrong,explain) in enumerate(specs):
  # deterministic rotation; correct letter varies; alternatives remain semantically distinct
  answers=[right]+wrong;shift=(module+i+grade)%4;choices=answers[-shift:]+answers[:-shift] if shift else answers
  # new, focused test for actual reading and NOT mere grade completion
  out.append({'id':f'q{i+1:02}','kind':kind,'type':'mcq','question':question,'options':choices,'correct':choices.index(right),'explanation':explain,'evidence':right if i<8 else c['limitation'], 'points':10})
 # Response prompts are assessed by parent or v3 provisional scorer; objective questions alone produce verified score.
 out.extend([
 {'id':'r01','kind':'short','type':'writing','question':f"In two or three sentences, explain how '{c['evidence1']}' relates to the idea that {c['hypothesis']}. Include a limitation.",
  'model':f"The observation that {c['evidence1']} is consistent with the hypothesis that {c['hypothesis']}. However, {c['limitation']}, so the explanation remains tentative.",
  'requiredEvidence':[stem,hyp,lim],'rubric':['State the hypothesized explanation accurately','Use the exact observation without changing its meaning','Name a genuine limit on the inference'],'points':0},
 {'id':'r02','kind':'synthesis','type':'writing','question':f"Compare Document A with the alternative view that {c['alternative']}. Where do the sources agree, and what would you test next?",
  'model':f"Both views can accept that {c['evidence1']}. They differ about whether {c['hypothesis']} or {c['alternative']}. A careful next study would use comparable observations to test the competing explanations.",
  'requiredEvidence':[stem,alt],'rubric':['Identify a shared observation','Present both claims fairly','Suggest a discriminating next observation'],'points':0},
 {'id':'r03','kind':'essay','type':'writing','question':f"Write a {'short spoken retelling or illustrated sentence' if grade<=1 else 'paragraph' if grade<=6 else 'one-page analytical response'} answering this case question: {c['question']}? Use two specific details, discuss an alternative, and close with the most defensible conclusion.",
  'model':f"The question at {c['place']} concerns {c['question']}. The observed record includes that {c['evidence1']} and that {c['evidence2']}. One explanation is that {c['hypothesis']}, although {c['alternative']}. Because {c['limitation']}, the sensible conclusion is provisional. The proposal that {c['intervention']} should be evaluated rather than assumed successful.",
  'requiredEvidence':[stem,other,alt,lim],'rubric':['Clearly answer the assigned question','Cite both concrete observations','Distinguish the rival explanation','Respect the limitation','Use organized, original wording'],'points':0},
 ])
 return out

def make_lesson(c,grade,level,idx):
 topicidx=idx%8
 sequence=idx//8
 m=sequence # learning sequence 0..7 for a single domain? Actually cases ordered by domain, 64 units. Use lesson progression per group of 8 across domain.
 focus=SKILLS[(idx+grade//2)%len(SKILLS)]
 p=main_paragraphs(c,grade,idx)
 cp=companion_paragraphs(c,grade)
 sp=source_paragraphs(c,grade)
 # 12 independent instructional micro-lessons, specific worked applications and follow-up; for early grade select 4, advanced 12.
 count=5 if grade<=1 else 7 if grade<=4 else 10 if grade<=8 else 12
 tutorials=[teacher_explanation(c,(idx+u+grade)%len(SKILLS),grade,u) for u in range(count)]
 # Supplemental independent rereading shifts target for 3 readings: annotations, worked example, evidence audit.
 annotations=[
 {'label':'Direct observation','quote':c['evidence1'],'why':'This describes a recorded detail rather than an explanation.'},
 {'label':'Second observation','quote':c['evidence2'],'why':'This detail adds context and may change a hypothesis.'},
 {'label':'Tentative explanation','quote':c['hypothesis'],'why':'This makes a claim about what may account for the observations.'},
 {'label':'Competing explanation','quote':c['alternative'],'why':'This cannot be ignored simply because it challenges the first idea.'},
 {'label':'Study limitation','quote':c['limitation'],'why':'This limits the scope of responsible conclusions.'},
 {'label':'Action proposal','quote':c['intervention'],'why':'A plan is not an evaluated outcome.'},
 ]
 texts=[
 {'title':c['title'],'genre':GENRES[idx%len(GENRES)],'paragraphs':p,'guidingQuestion':c['question'],'sourceLabel':'Original constructed reading · Document A'},
 {'title':'A second perspective','genre':'opinion / opposing view','paragraphs':cp,'guidingQuestion':'What can two reasonable readers disagree about?','sourceLabel':'Original constructed reading · Document B'},
 {'title':'Evidence packet and source notes','genre':'constructed primary-source dossier','paragraphs':sp,'guidingQuestion':'Which claims are observations, estimates, or recommendations?','sourceLabel':'Original classroom simulation · Records A–G'}
 ]
 questions=make_questions(c,grade,idx,level)
 # A printable writing rubric supports paragraphs and pages; no automatically generated writing grade claims accuracy.
 writingRubric=[
 {'name':'Understanding','weight':25,'criterion':'Explains the source question without inventing facts.'},
 {'name':'Evidence','weight':25,'criterion':'Uses two relevant, specific details from the text accurately.'},
 {'name':'Reasoning','weight':20,'criterion':'Explains how those details connect to the claim and considers another view.'},
 {'name':'Organization','weight':15,'criterion':'Has a comprehensible beginning, middle, and conclusion for this grade.'},
 {'name':'Language','weight':15,'criterion':'Uses readable sentences and age-appropriate conventions.'},
 ]
 # Deliberate learning: vocabulary + explicit instruction + worked examples + retrieval assignments + transfer task.
 vocab=[{'word':c['term'],'definition':c['definition'],'useInContext':f"The term {c['term']} is central to the question of {c['question']}."},
 {'word':'evidence','definition':'Information used to support or challenge a claim.','useInContext':f"The observation that {c['evidence1']} is evidence, not a final verdict."},
 {'word':'inference','definition':'An interpretation based on observations and reasoning.','useInContext':f"The idea that {c['hypothesis']} is an inference."},
 {'word':'limitation','definition':'A boundary on the strength or scope of a conclusion.','useInContext':f"Here, {c['limitation']}."}]
 # Follow-up activity gives legitimate skill transfer rather than answer-copying.
 transfer=[
 f"Think of a different problem at home or school. Write one direct observation before stating your explanation.",
 f"Write two hypotheses for the situation in {c['title']}. Describe an observation that would distinguish them.",
 f"Retell the case from the standpoint of someone who is skeptical of {c['intervention']}.",
 f"Explain why the numerical evidence '{c['measurement']}' does not automatically prove cause and effect.",
 f"Write an author note identifying the one sentence most likely to be overstated if a qualifier were removed.",
 f"List two questions that an independent reader would need answered before making a policy recommendation.",
 ]
 return {'id':f'{level}-R4-{idx+1:03}','level':level,'gradeOrder':grade,'sequence':idx,'title':c['title'],'domain':c['domain'],'skill':focus[0],
 'genre':GENRES[idx%len(GENRES)],'readingTarget':level_skill(grade),'estimatedMinutes':(10 if grade<=1 else 15 if grade<=4 else 25 if grade<=8 else 40),
 'factualStatus':'Fictional instructional scenario; all figures, quotations and reports are invented for practice.',
 'texts':texts,'instruction':tutorials,'annotations':annotations,'vocabulary':vocab,
 'questions':questions,'transferTasks':transfer,'writingRubric':writingRubric,
 'checkpoint':{'thresholdPercent':80,'objectiveQuestions':10,'mustReviewWriting':True,
   'meaning':'Objective comprehension can be marked exactly; a person must review the writing task before certifying broader proficiency.'},
 'lessonGoal':f"{focus[1]} Practice with {c['domain'].lower()} material: {c['question']}?"}

meta={'version':'4.0','title':'ATLAS College Reading Pathway','levels':[],'counts':{'levels':16,'units':0,'readings':0,'objectiveQuestions':0,'writingAssignments':0,'microLessons':0,'words':0},
      'courseStandard':'Original illustrative cases; teacher-reviewed writing and external assessments required to verify independent college reading mastery.',
      'skills':[{'title':a,'definition':b} for a,b in SKILLS]}
rows=[];sizes=[]
for level,levelname,grade in LEVELS:
 lessons=[make_lesson(c,grade,level,i) for i,c in enumerate(CASES)]
 d={'level':level,'name':levelname,'order':grade,'lessons':lessons}
 # fixed script globals, avoids fetch under file://. json inline wrapper.
 txt='window.ATLAS_PATHWAY_CONTENT=window.ATLAS_PATHWAY_CONTENT||{};window.ATLAS_PATHWAY_CONTENT['+json.dumps(level)+']=' + json.dumps(d,ensure_ascii=False,separators=(',',':'))+';\n'
 f=OUT/f'level_{level.lower()}.js';f.write_text(txt,encoding='utf-8')
 sizes.append((level,len(txt.encode('utf-8'))))
 for l in lessons:
  row={'level':level,'unit_id':l['id'],'domain':l['domain'],'skill':l['skill'],'title':l['title'],'reading_word_count':sum(len(re.findall(r"\b[\w']+\b",p)) for t in l['texts'] for p in t['paragraphs']),
  'objective_items':10,'writing_tasks':3,'tutorials':len(l['instruction'])}
  rows.append(row)
  meta['counts']['readings']+=len(l['texts']);meta['counts']['objectiveQuestions']+=10;meta['counts']['writingAssignments']+=3
  meta['counts']['microLessons']+=len(l['instruction']);meta['counts']['words']+=row['reading_word_count']
 meta['levels'].append({'id':level,'name':levelname,'order':grade,'units':len(lessons),'startSkill':level_skill(grade)})
 meta['counts']['units']+=len(lessons)
manifest='window.ATLAS_PATHWAY_MANIFEST='+json.dumps(meta,ensure_ascii=False,separators=(',',':'))+';\n'
(SRC/'pathway-v4'/'manifest.js').write_text(manifest,encoding='utf-8')
(SRC/'pathway-v4'/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'docs'/'V4_READING_CURRICULUM_INDEX.csv').parent.mkdir(parents=True,exist_ok=True)
with open(ROOT/'docs'/'V4_READING_CURRICULUM_INDEX.csv','w',newline='',encoding='utf-8') as fd:
 w=csv.DictWriter(fd,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print('SIZES:',sizes)
print('CONTENT TOTAL',sum(n for _,n in sizes),'bytes;',round(sum(n for _,n in sizes)/1024**2,2),'MiB')
print('COUNTS',meta['counts'])
