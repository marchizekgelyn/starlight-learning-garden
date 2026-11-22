/* ATLAS proofreading v3. Rules are opt-in mechanical suggestions, not a semantic grammar checker.
 * No network/AI; no broad corrections for dialect, homophones, names or quotations.
 */
(function(root,factory){const api=factory();if(typeof module!=='undefined'&&module.exports)module.exports=api;if(root)root.ATLAS_PROOFREAD_V3=api;})(typeof window!=='undefined'?window:null,function(){'use strict';
 const misspellings={
 alot:'a lot',adress:'address',adresses:'addresses',accomodate:'accommodate',acommodate:'accommodate',accomodation:'accommodation',acheive:'achieve',acrossed:'across',agressive:'aggressive',arguement:'argument',begining:'beginning',beleive:'believe',belive:'believe',becuase:'because',becasue:'because',buisness:'business',calender:'calendar',comming:'coming',comittee:'committee',concious:'conscious',definately:'definitely',definate:'definite',diferent:'different',dissapear:'disappear',embarass:'embarrass',enviroment:'environment',exagerate:'exaggerate',existance:'existence',experiance:'experience',familly:'family',finaly:'finally',foriegn:'foreign',fourty:'forty',freind:'friend',goverment:'government',grammer:'grammar',happend:'happened',harrass:'harass',hieght:'height',immediatly:'immediately',independant:'independent',intrest:'interest',knowlege:'knowledge',langauge:'language',liason:'liaison',libary:'library',lisence:'license',mispell:'misspell',neccessary:'necessary',noticable:'noticeable',occured:'occurred',occurence:'occurrence',oppinion:'opinion',paralell:'parallel',persue:'pursue',posession:'possession',prefered:'preferred',priviledge:'privilege',probaly:'probably',pronounciation:'pronunciation',recieve:'receive',recieved:'received',recieving:'receiving',recomend:'recommend',refered:'referred',relevent:'relevant',remeber:'remember',responce:'response',responsability:'responsibility',seperate:'separate',seperately:'separately',similer:'similar',sincerly:'sincerely',speach:'speech',succesful:'successful',suprise:'surprise',surpress:'suppress',teh:'the',thier:'their',thoght:'thought',tommorow:'tomorrow',truely:'truly',untill:'until',usefull:'useful',wierd:'weird',wich:'which',writting:'writing',writen:'written',woud:'would',yesturday:'yesterday'
 };
 const contractions={dont:"don't",cant:"can't",wont:"won't",isnt:"isn't",arent:"aren't",wasnt:"wasn't",werent:"weren't",doesnt:"doesn't",didnt:"didn't",wouldnt:"wouldn't",couldnt:"couldn't",shouldnt:"shouldn't",hadnt:"hadn't",hasnt:"hasn't",havent:"haven't",mustnt:"mustn't",neednt:"needn't",wasnt:"wasn't"};
 const safePatterns=[
 {rule:'Remove whitespace before punctuation',description:'No space is normally needed before a comma, period or question mark.',regex:/[ \t]+([,;:.!?])/g,replacement:m=>m[1]},
 {rule:'Reduce double spaces',description:'Standard prose normally uses one space between words.',regex:/ {2,}/g,replacement:()=> ' '},
 {rule:'Add space after comma',description:'Insert a space when a comma directly joins two words.',regex:/([a-z]),([a-z])/g,replacement:m=>m[1]+', '+m[2]},
 {rule:'Add space after semicolon',description:'Separate words following semicolons.',regex:/([a-z]);([a-z])/g,replacement:m=>m[1]+'; '+m[2]},
 {rule:'Capitalize stand-alone I',description:'Use a capital I for the first-person pronoun in standard English.',regex:/(^|[^\p{L}])i(?=[^\p{L}]|$)/gu,replacement:m=>m[1]+'I'},
 {rule:'Remove adjacent duplicate word',description:'A word may have been typed twice accidentally; read the result to confirm.',regex:/\b(the|and|with|for|of|is|was|were|a|to|from|on|at|in|that|this)\s+\1\b/gi,replacement:m=>m[1]},
 ];
 const escapeReg=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 const lexicalPattern=new RegExp('\\b('+Object.keys(misspellings).map(escapeReg).join('|')+')\\b','gi');
 const contractionPattern=new RegExp('\\b('+Object.keys(contractions).map(escapeReg).join('|')+')\\b','gi');
 function matchCase(before,after){if(before.toUpperCase()===before)return after.toUpperCase();if(before[0]===before[0].toUpperCase())return after[0].toUpperCase()+after.slice(1);return after;}
 function applyRule(text,regex,transform,rule,description,changes){return text.replace(regex,(...args)=>{const before=args[0],after=transform(args);if(before!==after){const index=args[args.length-2];changes.push({rule,before,after,position:typeof index==='number'?index:null,explanation:description});}return after;});}
 function proofread(input){let revised=String(input??''),changes=[];
 revised=applyRule(revised,lexicalPattern,a=>matchCase(a[0],misspellings[a[0].toLowerCase()]),'Common spelling mistake','This is a common spelling correction; make sure the intended word is unchanged.',changes);
 revised=applyRule(revised,contractionPattern,a=>matchCase(a[0],contractions[a[0].toLowerCase()]),'Missing contraction apostrophe','Add the apostrophe if a contraction is intended.',changes);
 for(const p of safePatterns){revised=applyRule(revised,p.regex,p.replacement,p.rule,p.description,changes);}
 return {revised,changed:revised!==String(input??''),changes:changes.slice(0,300),count:changes.length,note:'Review each suggested change before applying it. Proper names, dialect, quotations and intentional style are not errors. This is not a full grammar or semantic checker.'};}
 return {version:'3.0.0',proofread,misspellings,contractions};
});
