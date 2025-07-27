(defproject mia "0.1.0-SNAPSHOT"
  :description "MIA - Meta-Intelligence Agent Framework"
  :url "https://github.com/tuo-username/MIA"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  :dependencies [[org.clojure/clojure "1.11.1"]
                 [org.clojure/tools.cli "1.0.219"]        ; Versione corretta
                 [org.clojure/spec.alpha "0.3.218"]       ; Versione corretta
                 [org.clojure/core.async "1.6.673"]
                 [org.clojure/data.json "2.4.0"]
                 [org.clojure/math.numeric-tower "0.0.5"]
                 [org.clojure/math.combinatorics "0.1.6"]
                 [incanter "1.9.3"]
                 [cheshire "5.11.0"]
                 [http-kit "2.6.0"]
                 [compojure "1.7.0"]
                 [ring/ring-defaults "0.4.0"]
                 [environ "1.2.0"]]
  :main ^:skip-aot mia.cli
  :target-path "target/%s"
  :source-paths ["src"]
  :test-paths ["test"]
  :profiles {:uberjar {:aot :all
                      :jvm-opts ["-Dclojure.compiler.direct-linking=true"]}
             :dev {:dependencies [[midje "1.10.9"]]}})