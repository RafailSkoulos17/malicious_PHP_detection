## Web Crawling σε Python

Σκοπός μας είναι να κάνουμε crawl το DOM σελίδων που περιέχουν JavaScript, οπότε οι απλές λύσεις (τύπου BeautifulSoup, ActiveSoup κλπ) δεν μας κάνουν. Για το λόγο αυτό θα χρησιμοποιήσουμε Headless Browsers σε περιβάλλον Python που μπορούν να "παρσάρουν" και JavaScript. Η πιο δημοφιλής τέτοια λύση είναι το [Selenium](http://www.seleniumhq.org/) 

### Βήμα 1ο: Εγκατάσταση Selenium

Σε περιβάλλον Python 3

```angular2html
$ sudo pip3 install selenium
```

### Βήμα 2ο: Φόρτωση GeckoDriver

Επειδή θα χρησιμοποιήσουμε Firefox σε headless mode, θα πρέπει να φορτώσουμε την κατάλληλη έκοδση του GeckoDriver. Στην περίπτωση που έχουμε Firefox άνω της έκδοσης 55.0 και linux-amd64 διανομή, μας κάνει η έκδοση που υπάρχει στον φάκελο *driver/*, διαφορετικά κατεβάζουμε και αντικαθιστούμε τον driver με την κατάλληλη έκδοση για την αρχιτεκτονική μας [από εδώ](https://github.com/mozilla/geckodriver/releases).

### Bήμα 3ο: Εγκατάσταση Χ Virtual Frame-Buffer και PyVirtualDisplay

Για να μην "πετάει" στο script διαρκώς παράθυρα του browser όταν κάνει render τις σελίδες, θα σηκώσουμε ένα "εικονικό" X περιβάλλον όπου θα φορτώνονται τα παράθυρα του Firefox (αντί να φορτώνονται στο δικό μας). Στην περίπτωση που δεν έχουμε το πακέτο *xvfb* στο Ubuntu το εγκαθιστάμε:

```angular2html
$ sudo apt-get install xvfb
```

και μετά εγκαθιστούμε την αντίστοιχη βιβλιοθήκη της python

```angular2html
$ sudo pip3 install pyvirtualdisplay
```

Πηγή: https://stackoverflow.com/a/23447450