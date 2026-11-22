/* Interactive visual grammar, rhetoric, narrative and evidence labs.
 * All diagrams are rendered from hand-built SVG markup; no external CDN. */
(function(root){'use strict';
  const labs=[
   {id:'evidence',label:'Evidence chain',icon:'◎',title:'From a clue to a justified conclusion',description:'A claim needs a traceable detail, an explanation, and an honest boundary.',nodes:[
     {title:'OBSERVE',short:'What is stated?',example:'A text says the soil is wet.',tip:'Quote or paraphrase a traceable fact.'},
     {title:'CLAIM',short:'What does it suggest?',example:'Someone may have watered the garden.',tip:'Prefer a narrow conclusion.'},
     {title:'REASON',short:'How does it connect?',example:'Wet soil is consistent with watering.',tip:'Explain the link, not just the detail.'},
     {title:'QUALIFY',short:'What remains unknown?',example:'Rain could have wet the soil too.',tip:'Identify alternative explanations.'}]},
   {id:'sentence',label:'Sentence anatomy',icon:'Aa',title:'Build a sentence that carries meaning',description:'Learn the functions of subject, predicate, object and modification.',nodes:[
     {title:'SUBJECT',short:'Who or what?',example:'The careful reader',tip:'The subject names the central participant.'},
     {title:'PREDICATE',short:'What happens?',example:'examines',tip:'The finite verb anchors the statement.'},
     {title:'OBJECT',short:'What is affected?',example:'the evidence',tip:'Some verbs take an object; not all do.'},
     {title:'MODIFIER',short:'How / when / where?',example:'before drawing a conclusion',tip:'Place modifiers near what they describe.'}]},
   {id:'narrative',label:'Plot arc',icon:'⌁',title:'Follow how a story changes',description:'Plot development is a pattern of choices and consequences—not a fixed rule for every story.',nodes:[
     {title:'SETUP',short:'A world and a want',example:'A student needs a map.',tip:'Identify setting and the character’s goal.'},
     {title:'TENSION',short:'A problem emerges',example:'The map is incomplete.',tip:'Ask what prevents the character from succeeding.'},
     {title:'TURN',short:'A consequential choice',example:'The student asks for help.',tip:'Track the turning point and its motivation.'},
     {title:'OUTCOME',short:'A changed situation',example:'The missing path is identified.',tip:'Consider what was resolved and what was not.'}]},
   {id:'rhetoric',label:'Rhetorical choices',icon:'△',title:'Argument depends on audience and purpose',description:'Credibility, reasons, and emotion may work together, but none substitutes for verification.',nodes:[
     {title:'AUDIENCE',short:'Who needs to decide?',example:'A youth council',tip:'What does this audience care about?'},
     {title:'LOGOS',short:'Evidence and reasons',example:'The path lacks seating.',tip:'Check relevance and reasoning quality.'},
     {title:'ETHOS',short:'Trust and credibility',example:'A transparent site survey',tip:'Ask how expertise is established.'},
     {title:'PATHOS',short:'Human stakes',example:'Visitors need rest stops.',tip:'Emotion should not replace support.'}]},
   {id:'research',label:'Research pathway',icon:'◇',title:'Turn a question into a defensible answer',description:'Follow an accountable research process with source provenance and limits.',nodes:[
     {title:'QUESTION',short:'Make it answerable',example:'Who uses the local library?',tip:'Narrow scope, setting and time.'},
     {title:'SOURCE',short:'Find relevant records',example:'A library visits report',tip:'Record author, date and method.'},
     {title:'VERIFY',short:'Compare independent data',example:'Check against a second source',tip:'Identify sampling and contradictory evidence.'},
     {title:'CITE',short:'Show your trail',example:'Attribute the exact claim',tip:'Make findings retrievable and qualified.'}]},
   {id:'poetry',label:'Poetry studio',icon:'✦',title:'Notice how language creates an effect',description:'Sound and figurative language invite interpretations; explain your reading using exact lines.',nodes:[
     {title:'SOUND',short:'Rhythm and texture',example:'Tick, tap, tick',tip:'What do repetition and pauses do?'},
     {title:'IMAGE',short:'Sensory details',example:'A pale light on water',tip:'Which sense is most active?'},
     {title:'FIGURE',short:'An imaginative comparison',example:'The river is a mirror',tip:'What does the comparison emphasize?'},
     {title:'READING',short:'Interpret with evidence',example:'The still scene suggests calm',tip:'Acknowledge other plausible readings.'}]}
  ];
  const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  function renderSvg(lab,active){
    const coords=[[152,112],[457,112],[762,112],[1067,112]];
    const nodes=lab.nodes.map((n,i)=>{const [x,y]=coords[i],on=i===active;
      return `<g><rect x="${x-122}" y="${y-61}" width="244" height="122" rx="20" fill="${on?'#0d8298':'#152d47'}" stroke="${on?'#9beadf':'#4f6882'}" stroke-width="${on?3:1.5}"/><text x="${x}" y="${y-18}" fill="${on?'#fff':'#89d6ec'}" text-anchor="middle" font-size="19" font-weight="750">${esc(n.title)}</text><text x="${x}" y="${y+18}" fill="#e0f1fa" text-anchor="middle" font-size="16">${esc(n.short)}</text><text x="${x}" y="${y+46}" fill="#adc6d9" text-anchor="middle" font-size="12">${esc(i+1)} / 4</text></g>`;
    }).join('');
    const connectors=coords.slice(0,3).map((p,i)=>`<path d="M${p[0]+124} 112 H${coords[i+1][0]-125}" stroke="#6bd8e2" stroke-width="3" stroke-dasharray="5 6" marker-end="url(#arr)"/>`).join('');
    return `<svg viewBox="0 0 1220 315" class="lab-svg" role="img" aria-label="${esc(lab.title)}: four-step learning diagram"><defs><linearGradient id="lbg"><stop stop-color="#092039"/><stop offset="1" stop-color="#142d4d"/></linearGradient><marker id="arr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10" fill="#6bd8e2"/></marker></defs><rect width="1220" height="315" rx="28" fill="url(#lbg)"/>${connectors}${nodes}<text x="52" y="261" font-size="18" fill="#d5eaf6">EXAMPLE: ${esc(lab.nodes[active].example)}</text><text x="52" y="293" font-size="15" fill="#8bbacd">${esc(lab.nodes[active].tip)}</text></svg>`;
  }
  root.ATLAS_VISUALS={labs,renderSvg};
})(typeof window==='undefined'?globalThis:window);
