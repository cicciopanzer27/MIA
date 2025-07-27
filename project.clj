(defproject mia "0.1.0-SNAPSHOT"
  :description "MIA - Machine Intelligence Architecture"
  :url "https://github.com/cicciopanzer27/MIA"
  :license {:name "MIT License" ; O la licenza che preferisci
            :url "https://opensource.org/licenses/MIT"}

  ;; Dipendenze necessarie per il core
  :dependencies [[org.clojure/clojure "1.11.1"]
                 [org.clojure/data.json "2.5.0"]] ; Usiamo la versione più recente che avevi

  ;; Specifica dove si trova il codice sorgente
  :source-paths ["src"]

  ;; Punto di ingresso per l'applicazione (il nostro kernel/dispatcher )
  :main mia.core

  ;; Opzioni per la JVM, utili per performance
  :jvm-opts ["-Xmx1g"] ; Assegna 1GB di RAM massima alla JVM

  ;; Profilo per creare un eseguibile "uberjar" se necessario in futuro
  :profiles {:uberjar {:aot :all
                       :jvm-opts ["-Dclojure.compiler.direct-linking=true"]}})
