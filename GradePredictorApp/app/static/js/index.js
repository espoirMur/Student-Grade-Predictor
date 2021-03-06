// Auto resize input
function resizeInput() {
    $(this).attr('size', $(this).val().length);
}

$('input[type="text"], input[type="email"]')
    // event handler
    .keyup(resizeInput)
    // resize on page load
    .each(resizeInput);


console.clear();
// Adapted from georgepapadakis.me/demo/expanding-textarea.html
(function(){

  var textareas = document.querySelectorAll('.expanding'),

      resize = function(t) {
        t.style.height = 'auto';
        t.style.overflow = 'hidden'; // Ensure scrollbar doesn't interfere with the true height of the text.
        t.style.height = (t.scrollHeight + t.offset ) + 'px';
        t.style.overflow = '';
      },

      attachResize = function(t) {
        if ( t ) {
          console.log('t.className',t.className);
          t.offset = !window.opera ? (t.offsetHeight - t.clientHeight) : (t.offsetHeight + parseInt(window.getComputedStyle(t, null).getPropertyValue('border-top-width')));



          resize(t);

          if ( t.addEventListener ) {
            t.addEventListener('input', function() { resize(t); });
            t.addEventListener('mouseup', function() { resize(t); }); // set height after user resize
          }

          t['attachEvent'] && t.attachEvent('onkeyup', function() { resize(t); });
        }
      };

  // IE7 support
  if ( !document.querySelectorAll ) {

    function getElementsByClass(searchClass,node,tag) {
      var classElements = new Array();
      node = node || document;
      tag = tag || '*';
      var els = node.getElementsByTagName(tag);
      var elsLen = els.length;
      var pattern = new RegExp("(^|\\s)"+searchClass+"(\\s|$)");
      for (i = 0, j = 0; i < elsLen; i++) {
        if ( pattern.test(els[i].className) ) {
          classElements[j] = els[i];
          j++;
        }
      }
      return classElements;
    }

    textareas = getElementsByClass('expanding');
  }

  for (var i = 0; i < textareas.length; i++ ) {
    attachResize(textareas[i]);
  }

})();



// for the autocomplete function


 $(document).ready(function() {
  // the basics
  // ----------
  var schools = ['metanoia', 'mwanga', 'bakandja', 'maendeleo', 'sainte ursule', 'ngoma', 'majengo', 'faraja', 'himbi', 'kyeshero', 'zanner', 'uhuru', 'mont caemel', 'maranatha', 'amani', 'itig', 'moria', 'de goma', 'mikeno nc', 'chemchem', 'kalungu', 'autodidacte', 'anuarite', 'mama yetu', 'muhini', 'st joseph', 'kimbilio', 'uzima', 'ibanda', 'visoke', 'bulera', 'alfajiri', 'kalimba', 'itfm/bukavu', 'icl', 'mawato', 'matendo', 'ndahura', 'mont sinai', 'sayuni', 'saint paul', 'ndosho', 'nyabushongo', 'butembo', 'mukaba', 'malikia wa bingu', 'mikeno islamique', 'wima', 'totoro', 'lukanga', 'la fontaine', 'milima', 'mikeno isl', 'tuungane', 'fadhili', 'tupendane', 'saint marc', 'avenir', 'mgr kataliko', 'nyamukola', 'kashenda', 'de bukavu', 'kishanga', 'mwanga/ uvira', 'saint andre', 'kashofu', 'auto', 'gs kigali', 'iti gombe', 'kasali', 'Lwanga', 'idap isp bunia', 'kitsombiro', 'jikaze', 'kigonza', 'zawadi ya raisi', 'uenezaji', 'aigle de dieu', 'kambali', 'espoir1', 'saint michel', 'bemba gombo', 'de beni', 'pain de vie', 'hekima', 'mavuno', 'edap isp bkv', 'edap/isp', 'rutoboko', 'tumba', 'amen', 'mgr guido', 'communautaire du lac', 'i katwa', 'cirezi', 'maadibisho', 'lumiere', 'lwanzururu', 'action kusaidiya', 'kasika', 'gs mont sinai', 'Mugunga', 'vungi', 'itfm maendeleo', 'LWANGA', 'namurera', 'chidasa', 'bsangani', 'mahamba', 'katana', 'mama mulezi', 'complexe scolaire kyabo', 'kirikiri', 'la releve', 'de l\'unite', 'lasagesse', 'notre dame olame', 'edac/isgea', 'bahati', 'nyakasaza', 'gs 8 mars', 'gs la promise', 'itk mahamba', 'weza', 'amkeni', 'ziwa kivu', 'sainte famille', 'pilote de katana', 'tuendelee', 'bigilimani', 'la pereaux', 'shalom', 'Lycée Mwandu', 'mululu', 'lukuga', 'mont sionii', 'edap/isp bukavu', 'bagira', 'mululusake', 'masisi', 'eistein ujuzi', 'mgr guido maria conforti', 'groupe scolaire gilgali', 'tupendane fec', 'Institut BWANGA', 'nyantende', 'kamole', 'bulumbi', 'oicha', 'MUGUNGA', 'it kasabinyole', 'kimua', 'nidunga', 'mabula', 'matumaini', 'bimenya', 'uaminifu', 'etoile', 'bwindi', 'bukinanyana', 'petits génies', 'luka', 'mapema', 'azma', 'st augustin', 'lwanga bobandana', 'la sapiniere', 'tobongisa', 'itm kizito', 'rwabika', 'gs lumière du progrès', 'mushere', 'bandashe', 'kilimani', 'tumaini letu', 'kiribunye', 'kiraku', 'sebyera', 'mapendo', 'hodari', 'virunga/quartier', 'visogho', 'ufamandu', 'masikilizano', 'gs de la salle', 'amina', 'kanzulinzuli', 'kiyabo', 'frere alimba', 'mgr byaghene', 'ujasiri', 'imaki/kirumba', 'bethsaida', 'alpha', 'kahya cibanda', 'kisolokele', 'itc ngaliema', 'moyo safi', 'savana', 'bikuka', 'bakita', 'MWANDU', 'virunga', 'gs consulaire congolaise/rwanda', 'baraka', 'sake', 'de bagira', 'kirumba', 'savana school', 'thabiti', 'patemo', 'kalangala', 'nengapeta', 'buhimba', 'jiwe', 'veronique', 'home feyen', 'it bugabo', 'imani panzi', 'complexe scolaire mulezi', 'wapole', 'epsk/fomulac', 'utamaduni', 'edap/kasuku', 'kanyabayonga', 'les petits génies', 'bweremana', 'matanda', 'l mapema', 'la félicité', 'shaloom', 'belge', 'mulo', 'kyatenga', 'loyola', '61', 'gs tumba', 'alfa', 'kasheke', 'molière', 'Mwangaza', 'de bunia', 'mboga', 'lumiere du monde', 'edap/upn', 'wema', 'Mwanda', 'salama', 'neema kwetu', 'bwito', 'busimba', 'isoko', 'ruwenzori', 'isingo', 'fazili', 'kabalaka', 'kirimavolo', 'kalimabenge', 'Mwandu', 'rambo', 'techn. f. maendeleo', 'LYCEE MWANDU', 'muku', 'kausa', 'L MWANDU', 'tisiesi', 'bustani', 'st etienne', 'burhiba', 'BWANGA', 'tujenge', 'enano', 'complex scolaire la veronique', 'sauvetage', 'matolu', 'asseco', 'de kingasani ii', 'mgr henri pierrard', 'anuarite/kisangani', 'mandai', 'mehe', 'buramba', 'masiki', 'bambu', 'mont des oliviers', 'vuhika', 'révérend samba', 'lyliane', 'tabiti', 'gs asteria urafiki', 'macha', 'luanga', 'bobokoli', 'st michel', 'saint francois xavier', 'mayele', 'technique mapendano', 'itcb', 'Alleluya', 'kabila', 'aero', 'kyambogho', 'linzo', 'nduba', 'INST. MPINGA', 'nelson mandela', 'uvira', 'tshoka', 'kabolwa', 'notre dame de la jeunesse', 'fdf', 'petit séminaire mugeri', 'kiruli', 'matenda', 'bunyakiri', 'humule', 'moliere', 'ecl', 'nikisi', 'l\'amitie', 'lowa', 'Mwanzo', 'mambowa', 'kivako', 'autsau', 'muungano', 'katasoire', 'mbovote', 'pt seminaire tumaini letu', 'mungano', 'tsiesi', 'bushumba', 'maman sphie', 'akili', 'kitumaini', 'muhungano', 'zako', 'mama sarah', 'totro', 'makyase', 'complexe scolaire nova stella', 'de kalamu', 'kahumo', 'Institut MWANDA', 'insrtitut de masisi', 'technique de l’Étude sociale', 'mutambala', 'laudjo', 'itav bbo', 'utaniadun', 'musanga', 'kayanja', 'tetembwa', 'katudwe', 'kibali', 'Bungulu Beni', 'gihundu', 'ITM DE BOGA', 'mandayi', 'molende', 'ibanga', 'kavanda', 'I LWANGA', 'nyamianda', 'ebi', 'LYCEE MWINDA', 'lwiro', 'INST DE KATWA', 'kaya', 'elise', 'kiwele', 'lemera', 'epaf', 'tuha utala', 'z', 'gscc', 'wamaza', 'itav/mushweshwe', 'jjardin de fleurs', 'complexe scolaire asteria urafiki', 'luvango', 'maboso', 'kaoze', 'kuntwala', 'de kirumba', 'ilambula', 'chemchem ya uzima', 'odari', 'it salama', 'lunya', 'INSTITUT LWANGA', 'goupe scolaire mont sinai', 'lusaka', 'savana school international', 'mgr moke', 'tujikaze', 'ujumbe', 'rufunda', 'les vert', 'amani cebia', 'imara', 'technique ind. de mahamba', 'MWANGAZA', 'mapera', 'galaxie', 'taraja', 'katarina', 'dibasana', 'mashauri', 'de récupération de la gombe', 'lyce techn de la pleine', 'itve', 'mama mwilu', 'banza', 'Mbaga', 'INST LWANGA', 'bikuba', 'nyabiondo', 'le germe', 'MWENGA', 'mbolitini', 'bashu', 'lukeba', 'ibanga 2', 'singa', 'itav', 'ifendula', 'gilgali', 'okapi', 'mabalako', 'la charite divine', 'mfuki', 'babwise', 'itm', 'ruvunda', 'bokoro', 'namango', 'malula', 'de kindu', 'congolaise de bujumbura', 'kashali', 'les dibobol', 'mugeri', 'famila dei', 'camp fac', '54', 'esise/gisenyi', 'diabena', 'du lac/kamvivira', 'seamen', 'malende', 'meso', 'mutsoperwa', 'edak/goma', 'fatima', 'muhe', 'INSTITUT BWINZI', 'conglais (au burundi)', 'imani', 'vikanzu', 'lumumba', 'zuza', 'I DE BKV', 'de basoko', 'idambo', 'nzamiboko', 'kabanda', 'alliance ouest africaine', 'guido', 'umuja international french school', 'ovoa', 'kibabi', 'cibanda', 'namire', 'tusome', 'lycéé anuarité', 'umoja fs', 'rijumba', 'lukweti', 'l mapendo', 'source du savoir', '53', 'de la sucrerie de kiliba', 'saint vincent de paul', 'Institut NJANJA', 'losa', 'kaumo', 'groupe scol. ndbc de byumba', 'musienene', 'lumbishi', 'mama onja', 'aleluya', 'bokolo', 'kasalala', 'ruhamiro', 'du lac', 'bunyanga', 'lisalisi', 'edap isp walikale', 'MWANA', 'essi nyamirambo', 'bonsomi', 'ruharaga', 'mabakanga', 'Intitut ALLELUYA', 'john mabwindi', 'magherya', 'boyulu', 'matengenezo', 'bugarula', 'kifungo', 'idap isp rutshuru', 'kitunda', 'luapula', 'mapendo/ngese', 'ceago', 'Rwaraga', 'tmaini', 'kipushi', 'nsindo', 'mali', 'burhuza', 'karhale', 'itm tulizeni/kyondo', 'masapi', 'kitundu', 'bibwe', 'complexe scolaire de l\'unité', 'saint pierre apôtre', 'Institut de KATWA', 'tuzo', 'maendeleo de oicha', 'nyabibwe', 'mambo', 'kambale', 'mwajengo', 'kabale', 'kilambo', 'adventiste/bunia', 'isea', 'kanzanza', 'kando', 'wai wai', 'saint raphael', 'madame de seviniere', 'bundji', 'masanikilo', 'instituti ndosho', 'Institut MWANZO', 'ipp/beni', 'kamanyola', 'ahenée de butembo', 'safina', 'la vision', 'kantundwe', 'salamu', 'kashozi', 'etpm', 'itsu', 'auzi', 'NDEREMBI', 'itso', 'mont tshikenge', '1uto', 'cardinale etsou', 'imoteyiti', 'mlezi', 'matcha', 'tisiesi/karisimbi', 'g.s lemba', 'c,s, umoja', 'mwendu', 'bushumba kafubi', 'base', 'utfm', 'weza2', 'tsololo', 'kamagema', 'carmel', 'butumba', 'vihya', 'MWANGI', 'visolo', 'de la gombe', 'GRACIA', 'esengo', 'kayadja', 'ludaha', 'kasuo', 'msaada', 'mont kitenge', 'bethanie', 'bandari', 'saint mariya goritti'];


  options = ['pedagogie', 'commmerciale et adm', 'bio-chimie', 'sociale', 'latin philo', 'math-physique', 'commerciale informatique', 'nutr', 'mec gene', 'construction', 'elec indust', 'elec', 'coupe couture', 'electronique générale', 'inconnu', 'mecanique machines outils', 'vétérinaire', 'agrecole', 'secretariat', 'machine outil', 'hotesse d\'acceuil', 'agronomie', 'batiment', 'hospitalière', 'economie', 'diet', 'fdf', 'industrielle', 'relations publiques', 'imprimerie'];
  var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
      var matches, substringRegex;

      // an array that will be populated with substring matches
      matches = [];

      // regex used to determine if a string contains the substring `q`
      substrRegex = new RegExp(q, 'i');

      // iterate through the pool of strings and for any string that
      // contains the substring `q`, add it to the `matches` array
      $.each(strs, function(i, str) {
        if (substrRegex.test(str)) {
          matches.push(str);
        }
      });

      cb(matches);
    };
  };


  $('#SCHOOL_RIGHT').typeahead({
    minLength: 1,
    fitToElement :true,
    source: substringMatcher(schools)
  });

  $('#OPTION_RIGHT').typeahead({
    minLength: 1,
    fitToElement :true,
    source: substringMatcher(options)
  });

});
