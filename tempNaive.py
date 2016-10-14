# -*- coding: utf-8 -*-
"""Sentiment analysis implementations.

.. versionadded:: 0.5.0
"""
from __future__ import absolute_import
from collections import namedtuple
import pigeo
from textblob import Blobber
import nltk

from textblob.en import sentiment as pattern_sentiment
from textblob.tokenizers import word_tokenize
from textblob.decorators import requires_nltk_corpus
from textblob.base import BaseSentimentAnalyzer, DISCRETE, CONTINUOUS
from textblob.classifiers import NaiveBayesClassifier
import pickle


class PatternAnalyzer(BaseSentimentAnalyzer):
    """Sentiment analyzer that uses the same implementation as the
    pattern library. Returns results as a named tuple of the form:

    ``Sentiment(polarity, subjectivity)``
    """

    kind = CONTINUOUS
    #: Return type declaration
    RETURN_TYPE = namedtuple('Sentiment', ['polarity', 'subjectivity'])

    def analyze(self, text):
        """Return the sentiment as a named tuple of the form:
        ``Sentiment(polarity, subjectivity)``.
        """
        return self.RETURN_TYPE(*pattern_sentiment(text))


def _default_feature_extractor(words):
    """Default feature extractor for the NaiveBayesAnalyzer."""
    return dict(((word, True) for word in words))


class NaiveBayesAnalyzer(BaseSentimentAnalyzer):
    """Naive Bayes analyzer that is trained on a dataset of movie reviews.
    Returns results as a named tuple of the form:
    ``Sentiment(classification, p_pos, p_neg)``

    :param callable feature_extractor: Function that returns a dictionary of
        features, given a list of words.
    """

    kind = DISCRETE
    #: Return type declaration
    RETURN_TYPE = namedtuple('Sentiment', ['classification', 'p_pos', 'p_neg'])

    def __init__(self, feature_extractor=_default_feature_extractor):
        super(NaiveBayesAnalyzer, self).__init__()
        self._classifier = None
        self.feature_extractor = feature_extractor

    @requires_nltk_corpus
    def train(self):
        """Train the Naive Bayes classifier on the movie review corpus."""
        super(NaiveBayesAnalyzer, self).train()
        neg_ids = nltk.corpus.movie_reviews.fileids('neg')
        pos_ids = nltk.corpus.movie_reviews.fileids('pos')
        neg_feats = [(self.feature_extractor(
            nltk.corpus.movie_reviews.words(fileids=[f])), 'neg') for f in neg_ids]
        pos_feats = [(self.feature_extractor(
            nltk.corpus.movie_reviews.words(fileids=[f])), 'pos') for f in pos_ids]
        train_data = neg_feats + pos_feats
        self._classifier = nltk.classify.NaiveBayesClassifier.train(train_data)

    def analyze(self, text):
        """Return the sentiment as a named tuple of the form:
        ``Sentiment(classification, p_pos, p_neg)``
        """
        # Lazily train the classifier
        super(NaiveBayesAnalyzer, self).analyze(text)
        tokens = word_tokenize(text, include_punc=False)
        filtered = (t.lower() for t in tokens if len(t) >= 3)
        feats = self.feature_extractor(filtered)
        prob_dist = self._classifier.prob_classify(feats)
        return self.RETURN_TYPE(
            classification=prob_dist.max(),
            p_pos=prob_dist.prob('pos'),
            p_neg=prob_dist.prob("neg")
        )


# with open('fullCorpusTrain.csv', 'r') as fp:
#     cl = NaiveBayesClassifier(fp, format="csv")
#     with open('fullCorpusTest.csv', 'r') as fptest:
#         print cl.accuracy(fptest)

from textblob import TextBlob
algo = ["@Apple Siri is witchcraft.  What next @googleresearch. 2 yr lead lost?",
"Bummer!  My @Yahoo! iPad fantasy football app keeps crashing; not sure if it the app or the new @apple iOS 5. Only two apps running.",
"@nansen Man, that sux! @apple io5 upgrade a total #fail for you!",
"RT @SHlFT: dear #google & #samsung... learn some presentation 101 first. please.",
"Dear @apple please send me my Mac Book back surely the repair is done by now... Thanks!",
"RT @DariuszPorowski: RT Me too! @rem8: On my way home from 1st day of #MTS11. Had great time with @alead @DariuszPorowski and others #mv ...",
"iTunes is @apple worst product. Worse than the #Newton or the hockey puck mouse. It utterly painful to use.",
"Not greatly impressed with #Google and #Samsung presentation skills.",
"hey @apple I hate my computer i need a #mack wanna send me a free one.",
"Fantastic work from #Samsung and #Google on the #GalaxyNexus superphone and the new #Android #ICS. Very impressive.",
"RT @LCmediaHouse: 4chan Chris Poole: #Facebook & #Google Are Doing It Wrong http://t.co/ZIxfa91N | via @RWW #socialmedia",
"Great, live contact management, quick contact card, add people directly to.your home screen #Android4.0 #Google",
"@Mayati I think @Apple didn't do such a thorough job with the step x steps for upgrade and move to iCloud. Now it cost me mightily.",
"Too bad #google didn't have a tribute graphic for #DennisRitchie.",
"Hey @apple, the SMS full message is complete shit. Yes, I'm annoyed.",
"Google ICS looks awesome, can't wait til it gets ported over to my evo, face unlock?! ... #android #google",
"#TwitterMalfunctioningAgain",
"RT @Assim99: Dear #Google, I want the Galaxy Nexus NOW. Please send it to me by email or something - I know you have the technology",
"Reader 'Tronman' compares #SteveBallmer to an albatross around #Microsoft neck.  Do you agree?  Join the discussion! http://t.co/Mn39R2vc",
"Sorry @apple, but #iMessage will never be what #BBM is. Disappointed.",
"So glad #Google adopted a design philosophy for #Android 4.0 a.k.a It shows soooo much! This is the polish I've been waiting for!",
"#twitter addict :)",
"Which planet is he living on? #Microsoft #CEO #Fail #palmface http://t.co/3zcq60SF",
"Can't wait until I can visit the holodeck! Thanks for sharing. RT @karljuhlke Beam me up #Microsoft! Microsoft has... http://t.co/ZGbk3xnK",
"#ThingsWeAllHate that person that acts like they know every fucking thing bitch you not #Google",
"So glad that I paid $69 for this @apple care protection plan.  Been on hold for over 20 minutes now.  Great customer service. #NOT",
"Also @EricGreenspan, don't forget @Apple stop closing the app store after each bloody purchase...",
"Just apply for a job at @Apple, hope they call me lol",
"Ready for some Ice Cream Sandwich! #google #android",
"RT @TripLingo: We're one of a few Featured Education Apps on the @Apple **Website** today, sweet! http://t.co/0yWvbe1Z",
"Camera app now has Panorama capabilities! #Google #Android #ICS",
"Blog Post: Cool Tool : Microsoft Mouse Without Borders. http://t.co/uM860jFh #Tools #Utilities #microsoft",
"facial recognition failed #IceCreamSandwich jajajajajajaj #FacialUnlock #samsumg #Google",
"ICS on the Galaxy Nexus has very smooth and responsive screen and widget navigation. #Google #Android #ICS",
"The face recognition unlock would be cool if it works. #android #google #icecreamsandwich",
"#skype is ruining the friendship with your aggressive #microsoft type selling. If i need something i'll ask. Thank you...",
"RT @radlerc: Yellowgate? Some iPhone 4S Users Complain of Yellow Tint to Screen http://t.co/uaqrxTNk @apple @iphone4s",
"@adiman_ #google #fail",
"My @Apple @macbook keyboard will not type :(",
"#Microsoft just bought #Skype officially. So how the future of #Skype on any other devices/operating systems? :(",
"I gotta say, Google got some pretty catchy advertisements for Android and Chrome. #google #android",
"All I can say about @Apple right now is #GoodRiddance  See? Cancer isn't ALL BAD!",
"Good support fm Kevin @apple #Bellevue store 4 biz customers TY!",
"OMG the #Android 4.0 SDK is available NOW @ http://t.co/OeUrmtLX!! #Google",
"@apple WTF why can we not add the newsstand to a folder?! We are already in your walled garden, so please don't remind us of it.",
"We need dates! #google #samsung #launchfail",
"I would be a lot happier if #Microsoft Word didn't freeze every 5 minutes.",
"#Update #Microsoft MS11-078 - Critical : Vulnerability in .NET Framework and Microsoft Silverlight Could Allow R... http://t.co/izO0WUNt",
"#IceCreamSandwich went way and beyond what I expected. Can't wait to get it on my Nexus to play with! #Google",
"New Galaxy Nexus: App Improvements -  Inbuilt Panoramic Pictures #nexus #samsung #google #android bit.ly/nEJbyE",
"9% now on my second full charge of the day. Pissed @Apple",
"@guardiantech I love the And now it is looking to China: Apple funds sweatshops there while Gates funds a foundation #apple #microsoft",
"With #Windows 8, #Microsoft can't forget past antitrust issues http://t.co/z4jWLQVu",
"#Microsoft Lync crash issue on #Mac OS X 10.7.2 [Fixed] - http://t.co/Gjiu2zz1",
"for some reason #twitter isnt allowing me to see my tweets that got retweeted.",
"God Bless @YouTube, @apple for  #appletv & our bad ass system. LOVING #PrincessOfChina. GB to @coldplay & @rihanna too :)",
"Well... @Paging_Dr_A has gotten back on #twitter.. there goes my TL lol",
"RT @JoelBurns: Dear @Apple, it me again. Thank for beautiful new iOS features. But I miss some of the old ones. Lk making calls & texts &gt;(",
"@apple What the point of iCloud wireless updates when ios5 now forces me to use the computer to charge my ipod touch now? #worstupdateever",
"@Apple - why do I have to have apps I am updating in their original 'folder' location? That was painful.",
"This is how charity works these days. http://t.co/839klkFH #billgates #philanthropy #microsoft",
"#iCloud set up was flawless and works like a champ! To the Cloud @Apple",
"#twitter why must you be so difficult?",
"So @PhoenixSwinger  iPhone 4 is giving her a hella hard time w/ the iOS5 update @apple",
"@ryanbaldwin @apple So in iTunes I go Store  Authorise why doesn't it just auto-authorise it when I sign into iTunes? Grrrr...",
"Soon. Getting ready for the party. #google #android #icecreamsandwich http://t.co/eZjCzLt6",
"@apple does iOS 5 rape your battery life? or am I just using my phone a lot since getting it",
"Microsoft Stores offer up free Windows Phone 7 devices #microsoft #microsoftstores http://t.co/7YvJMHnQ",
"#Twitter y #Facebook OFF",
"#Samsung, #Google Unveil Phone http://t.co/hOB37hbO",
"Maybe not the most efficient way to browse, but fun: #Google releases an Infinite Digital Bookcase http://t.co/X1qzeX7f by @MeghanKel",
"One would think the voice recognition on the @apple tech support line would work a little better.",
"I wish the Apple updater would stop trying to ram iTunes down my throat. I don't own a pissing iPhone @apple",
"#twitter still not showin my mothafuckin #retweets . .",
"_ibertaddigital.tv/ iPad a briliant SteveJobs produck ,http://t.co/00ohfLY6 @Apple present... http://t.co/DBbWSDpx",
"@kursed #Google is terrible at presentations. Hated the terrible camera interference from the huge screen behind the speakers. #headache",
"Oh, just fuck you, @apple. Already?? ---&gt;  iPhone 5 on schedule for summer launch? http://t.co/Ofh9PTaG via @BGR",
"Raise your hand if you now want an #Android4 #IceCreamSandwich powered #GALAXYNexus phone! #Google #Samsung",
"@apple why isn't my iTunes updating? I just wanna update my iPhone to IOS5!!! Then iTunes says that it needs to update to do it. Then fails!",
"@BrianMincey @apple the chipsets tear through battery life. Coworker has a htc thunderbolt that he gets about 3 hours of life.",
"Data Usage feature looks amazing and useful! #Google #GalaxyNexus",
"@RickySinghPT got a new backside for my eye phone! V impressed with @apple",
"@Joelplane @apple I hear you! I've had trouble with my 3 & now 4. I've even turned down brightness. #andshuttingdownrunningprograms #nohelp",
"RT @CBM: Lies @apple. the battery on this new iPhone4S is definitely not any better.",
"#Microsoft #Windows Media Centre GUI #Fail #MajorFail",
".@apple thanks for fixing this... http://t.co/wTj1ogDO",
"Finally got the @apple IPhone thanks to @sprint getting with the times",
"Why book @Apple Genius Bar if after 2.5 hours you still can't be served. Disappointing Apple Store Sydney. #thanksfornothing",
"#Retweets section of my #twitter account has not been working for 17 hours! Is Everyone else having this problem? #RT #RTs",
"New contact app builds on a magazine style layout and aggregates contact info from multiple sources. Very slick. #Google #Android #ICS",
"#microsoft fail #notresponding for fcucks sake  http://t.co/lCXa9q8P",
"RT @amarsanghera The fact that #Microsoft are using a #QRCode alongside one of their colour code shows the format is failing, opinions",
"Just participated in another #Microsoft #SQLServer certification test with #TSQL typing instead of multiple choices. Really cool.",
"#Microsoft took 6 months to recruit Everson and 9 months to lose her to #Faceboook via Adweek http://t.co/l5mTm6Ig",
"not happy with @apple right now. the upgrade to my itouch4 took out my itouch and laptop. #help",
"@Tita_Ramos #Google it =)",
"Mmm... #SmarterPhone RT @Android: Introducing Ice Cream Sandwich, the delicious new version of Android: http://t.co/AXl2K1Gs #ICS #google",
"Spoke to an @Apple rep on phone & could hear her tv blaring in the bg.  She said, I cant actually help u, just direct u back to the web"]
# for tweet in algo:
#     blob = TextBlob(tweet)
#     print blob.sentiment[0]
class NaiveBayesAnalyzerWLM(BaseSentimentAnalyzer):
    """Naive Bayes analyzer that is trained on a dataset of movie reviews.
    Returns results as a named tuple of the form:
    ``Sentiment(classification, p_pos, p_neg)``

    :param callable feature_extractor: Function that returns a dictionary of
        features, given a list of words.
    """

    kind = DISCRETE
    #: Return type declaration
    RETURN_TYPE = namedtuple('Sentiment', ['classification', 'p_pos', 'p_neg'])

    def __init__(self, feature_extractor=_default_feature_extractor):
        super(NaiveBayesAnalyzerWLM, self).__init__()
        self._classifier = None
        self.feature_extractor = feature_extractor

    @requires_nltk_corpus
    def train(self):
        """Train the Naive Bayes classifier on the movie review corpus."""
        super(NaiveBayesAnalyzerWLM, self).train()
        with open('fullCorpusTrain.csv', 'r') as fp:
            self._classifier = NaiveBayesClassifier(fp, format="csv")

    def analyze(self, text):
        """Return the sentiment as a named tuple of the form:
        ``Sentiment(classification, p_pos, p_neg)``
        """
        # Lazily train the classifier
        super(NaiveBayesAnalyzerWLM, self).analyze(text)
        tokens = word_tokenize(text, include_punc=False)
        filtered = (t.lower() for t in tokens if len(t) >= 3)
        feats = self.feature_extractor(filtered)
        prob_dist = self._classifier.prob_classify(feats)
        return self.RETURN_TYPE(
            classification=prob_dist.max(),
            p_pos=prob_dist.prob('pos'),
            p_neg=prob_dist.prob("neg")
        )

# analyzer = NaiveBayesAnalyzerWLM()
# analyzer.train()
# f = open('my_classifier.pickle', 'wb')
# pickle.dump(analyzer, f)
# f.close()
f = open('my_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()
tb = Blobber(analyzer=classifier)
for tweet in algo:
    blob = tb(tweet)
    bayes_sentiment = blob.sentiment
    print bayes_sentiment.classification
#     with open('fullCorpusTest.csv', 'r') as fptest:
#         print cl.accuracy(fptest)