/* What the laws and sections named in NCRB's tables are about.
 *
 * NCRB's columns name crimes by statute and section ("Sec. 66 IT Act",
 * "Dowry deaths (Sec. 304B IPC)"). explain(text, context) finds the sections
 * and Acts mentioned and returns a one-line description of each. The Act is
 * read from the text itself, or from the table title passed as context;
 * a bare section number is taken as the Indian Penal Code (IPC), which is
 * what Crime in India means by default. From July 2024 the IPC was replaced by
 * the Bharatiya Nyaya Sanhita (BNS); sections are renumbered there.
 *
 * Descriptions are summaries of what each provision covers, written for
 * readers; they are not the statutory text.
 */

const IPC = {
  '120B': 'criminal conspiracy', 121: 'waging war against the Government of India', '124A': 'sedition',
  147: 'rioting', 148: 'rioting armed with a deadly weapon', '153A': 'promoting enmity between groups',
  279: 'rash driving or riding on a public way', 302: 'murder', 304: 'culpable homicide not amounting to murder',
  '304A': 'causing death by negligence (includes most road deaths)', '304B': 'dowry death', 305: 'abetment of suicide of a child or a person of unsound mind',
  306: 'abetment of suicide', 307: 'attempt to murder', 308: 'attempt to commit culpable homicide', 309: 'attempt to commit suicide',
  312: 'causing miscarriage', 313: 'causing miscarriage without the woman’s consent', 315: 'act to prevent a child being born alive or to cause its death after birth',
  316: 'causing death of a quick unborn child', 317: 'exposure and abandonment of a child under twelve', 318: 'concealment of birth by secret disposal of the body',
  323: 'voluntarily causing hurt', 324: 'causing hurt by dangerous weapons or means', 325: 'voluntarily causing grievous hurt',
  326: 'grievous hurt by dangerous weapons or means', '326A': 'acid attack', '326B': 'attempted acid attack',
  341: 'wrongful restraint', 342: 'wrongful confinement', 354: 'assault or criminal force on a woman with intent to outrage her modesty',
  '354A': 'sexual harassment', '354B': 'assault with intent to disrobe a woman', '354C': 'voyeurism', '354D': 'stalking',
  363: 'kidnapping', '363A': 'kidnapping or maiming a minor for begging', 364: 'kidnapping or abduction in order to murder',
  '364A': 'kidnapping for ransom', 365: 'kidnapping with intent to wrongfully confine', 366: 'kidnapping or abducting a woman to compel marriage',
  '366A': 'procuration of a minor girl', '366B': 'importation of a girl from a foreign country', 367: 'kidnapping to subject a person to grievous hurt or slavery',
  368: 'concealing a kidnapped person', 369: 'kidnapping a child under ten to steal from it', 370: 'trafficking of persons',
  '370A': 'exploitation of a trafficked person', 372: 'selling a minor for prostitution', 373: 'buying a minor for prostitution',
  376: 'rape', '376A': 'rape causing death or a persistent vegetative state', '376B': 'sexual intercourse by a husband with his wife during separation',
  '376C': 'sexual intercourse by a person in authority', '376D': 'gang rape', '376E': 'repeat offender (rape)',
  377: 'unnatural offences (read down by the Supreme Court in 2018 for consenting adults)', 379: 'theft', 380: 'theft in a dwelling house',
  382: 'theft after preparation to cause death or hurt', 384: 'extortion', 392: 'robbery', 393: 'attempt to commit robbery',
  394: 'causing hurt in committing robbery', 395: 'dacoity', 396: 'dacoity with murder', 397: 'robbery or dacoity with attempt to cause death or grievous hurt',
  399: 'making preparation to commit dacoity', 402: 'assembling to commit dacoity', 406: 'criminal breach of trust', 409: 'criminal breach of trust by a public servant, banker or agent',
  411: 'dishonestly receiving stolen property', 420: 'cheating', 435: 'mischief by fire or explosive', 436: 'mischief by fire with intent to destroy a house',
  447: 'criminal trespass', 448: 'house-trespass', 454: 'lurking house-trespass or house-breaking', 457: 'lurking house-trespass or house-breaking by night',
  465: 'forgery', 467: 'forgery of a valuable security or will', 468: 'forgery for the purpose of cheating', 471: 'using a forged document as genuine',
  '489A': 'counterfeiting currency notes or bank notes', '489B': 'using forged currency notes as genuine', '489C': 'possessing forged currency notes',
  494: 'bigamy', '498A': 'cruelty by husband or his relatives', 506: 'criminal intimidation', 509: 'word, gesture or act intended to insult the modesty of a woman',
};

const IT = {
  43: 'damage to a computer or computer system (civil compensation)', 65: 'tampering with computer source documents',
  66: 'computer-related offences, including hacking (dishonestly or fraudulently doing an act in section 43)',
  '66A': 'sending offensive messages through a communication service (struck down by the Supreme Court in 2015)',
  '66B': 'dishonestly receiving a stolen computer resource or device', '66C': 'identity theft (using someone’s password, signature or other identity)',
  '66D': 'cheating by personation using a computer resource', '66E': 'violation of privacy: capturing or publishing private images',
  '66F': 'cyber terrorism', 67: 'publishing or transmitting obscene material in electronic form', '67A': 'publishing or transmitting sexually explicit material',
  '67B': 'publishing or transmitting material depicting children in sexually explicit acts', 68: 'failure to comply with a direction of the Controller',
  69: 'failure to assist interception, monitoring or decryption ordered by the Government', 70: 'unauthorised access to a protected system',
  71: 'misrepresentation to obtain a licence or digital signature certificate', 72: 'breach of confidentiality and privacy',
  '72A': 'disclosure of information in breach of a lawful contract', 73: 'publishing a false digital signature certificate',
  74: 'publishing a digital signature certificate for a fraudulent purpose',
};

const BNS = {
  64: 'rape', 70: 'gang rape', 74: 'assault or criminal force on a woman with intent to outrage her modesty', 78: 'stalking', 79: 'word, gesture or act intended to insult the modesty of a woman',
  80: 'dowry death', 85: 'cruelty by husband or his relatives', 103: 'murder', 106: 'causing death by negligence', 108: 'abetment of suicide', 109: 'attempt to murder',
  111: 'organised crime', 113: 'terrorist act', 137: 'kidnapping', 143: 'trafficking of persons', 303: 'theft', 304: 'snatching', 309: 'robbery', 310: 'dacoity', 316: 'criminal breach of trust', 318: 'cheating',
};

const POCSO = {
  4: 'penetrative sexual assault on a child', 6: 'aggravated penetrative sexual assault on a child', 8: 'sexual assault on a child',
  10: 'aggravated sexual assault on a child', 12: 'sexual harassment of a child', 14: 'using a child for pornographic purposes', 15: 'storing child pornographic material',
  17: 'abetment of an offence under the Act', 21: 'failure to report or record an offence',
};

/* Acts named in NCRB's tables, in a sentence each. */
const ACTS = [
  [/\bIPC\b|indian penal code/i, 'IPC', 'Indian Penal Code, 1860: the main criminal law until 30 June 2024, when the Bharatiya Nyaya Sanhita (BNS) replaced it.'],
  [/\bBNS\b|nyaya sanhita/i, 'BNS', 'Bharatiya Nyaya Sanhita, 2023: replaced the Indian Penal Code from 1 July 2024, with renumbered sections.'],
  [/\bI\.?\s?T\.?\s+Act|information technology act/i, 'IT Act', 'Information Technology Act, 2000: offences involving computers and electronic records.'],
  [/pocso|protection of children from sexual offences/i, 'POCSO', 'Protection of Children from Sexual Offences Act, 2012: sexual offences against anyone under 18.'],
  [/\bSC\/ST\b|prevention of atrocities|\bPoA\b/i, 'SC/ST (PoA) Act', 'Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act, 1989: offences committed against Dalits and Adivasis because of their caste or tribe.'],
  [/protection of civil rights|\bPCR\b/i, 'PCR Act', 'Protection of Civil Rights Act, 1955: practising or enforcing untouchability.'],
  [/dowry prohibition/i, 'Dowry Prohibition Act', 'Dowry Prohibition Act, 1961: giving, taking or demanding dowry.'],
  [/immoral traffic|\bITPA\b|\bI\.?T\.?\s?\(?P\)?\s?Act/i, 'ITP Act', 'Immoral Traffic (Prevention) Act, 1956: trafficking for commercial sexual exploitation.'],
  [/domestic violence/i, 'PWDV Act', 'Protection of Women from Domestic Violence Act, 2005: a civil law; NCRB counts breaches of protection orders.'],
  [/indecent representation/i, 'IRW Act', 'Indecent Representation of Women (Prohibition) Act, 1986.'],
  [/sati/i, 'Sati Prevention Act', 'Commission of Sati (Prevention) Act, 1987.'],
  [/child marriage/i, 'PCM Act', 'Prohibition of Child Marriage Act, 2006 (Child Marriage Restraint Act, 1929, before it).'],
  [/\bNDPS\b|narcotic drugs/i, 'NDPS Act', 'Narcotic Drugs and Psychotropic Substances Act, 1985.'],
  [/arms act/i, 'Arms Act', 'Arms Act, 1959: possession and use of firearms without a licence.'],
  [/explosive/i, 'Explosives Acts', 'Explosive Substances Act, 1908, and Explosives Act, 1884.'],
  [/juvenile justice|\bJJ Act/i, 'JJ Act', 'Juvenile Justice (Care and Protection of Children) Act: children in conflict with the law, and offences against children such as cruelty.'],
  [/\bUAPA\b|unlawful activities/i, 'UAPA', 'Unlawful Activities (Prevention) Act, 1967: terrorism and unlawful associations.'],
  [/prevention of corruption/i, 'PC Act', 'Prevention of Corruption Act, 1988: bribery and corruption by public servants.'],
  [/motor vehicles act/i, 'MV Act', 'Motor Vehicles Act, 1988.'],
  [/excise/i, 'Excise Acts', 'State Excise Acts: illicit liquor.'],
  [/gambling/i, 'Gambling Acts', 'State Gambling Acts and the Public Gambling Act, 1867.'],
  [/bonded labour/i, 'BLSA Act', 'Bonded Labour System (Abolition) Act, 1976.'],
  [/child labour/i, 'Child Labour Act', 'Child and Adolescent Labour (Prohibition and Regulation) Act, 1986.'],
  [/\bSLL\b|special (and|&) local laws/i, 'SLL', 'Special and Local Laws: crimes under laws other than the IPC/BNS, such as the Arms, NDPS, Excise and Gambling Acts.'],
];

function lawOf(text, context) {
  const t = `${text} ${context || ''}`;
  if (/\bI\.?\s?T\.?\s+Act|information technology/i.test(text)) return 'IT';
  if (/pocso/i.test(text)) return 'POCSO';
  if (/\bBNS\b|nyaya sanhita/i.test(text)) return 'BNS';
  if (/\bIPC\b|penal code/i.test(text)) return 'IPC';
  if (/\bI\.?\s?T\.?\s+Act|information technology|cyber/i.test(context || '')) return 'IT';
  if (/pocso/i.test(context || '')) return 'POCSO';
  if (/\bBNS\b|nyaya sanhita/i.test(context || '')) return 'BNS';
  return /\bact\b/i.test(t) && !/\bIPC\b/i.test(t) ? null : 'IPC';
}

const TABLES = { IPC, IT, BNS, POCSO };
const NAMES = { IPC: 'IPC', IT: 'IT Act', BNS: 'BNS', POCSO: 'POCSO Act' };

/** [{label, text}] for every section and Act named in `text` (context: the table title). */
export function explain(text, context = '') {
  const out = [];
  const seen = new Set();
  const s = String(text || '');
  const secRx = /(?:\bsec(?:tion)?s?\.?|\bu\/s\.?|\bs\.)\s*((?:\d{1,3}[A-F]?(?:\s*\(\d+\))?)(?:\s*(?:,|&|\/|and|to|-)\s*\d{1,3}[A-F]?(?:\s*\(\d+\))?)*)/gi;
  let m;
  while ((m = secRx.exec(s))) {
    const law = lawOf(s, context);
    const tab = law && TABLES[law];
    if (!tab) continue;
    for (const n of m[1].split(/\s*(?:,|&|\/|and|to|-)\s*/)) {
      const num = n.replace(/\s*\(\d+\)/, '').toUpperCase();
      const k = `${law}:${num}`;
      if (seen.has(k) || !(num in tab)) continue;
      seen.add(k);
      out.push({ label: `Section ${num} ${NAMES[law]}`, text: tab[num] });
    }
  }
  for (const [rx, label, text2] of ACTS) {
    if (rx.test(s) && !seen.has(label)) { seen.add(label); out.push({ label, text: text2 }); }
  }
  return out;
}

/** The same, for many labels at once, without repeats. */
export function explainAll(labels, context = '') {
  const seen = new Set(), out = [];
  for (const l of labels) for (const e of explain(l, context)) if (!seen.has(e.label)) { seen.add(e.label); out.push(e); }
  return out;
}
