(ns mia.cli
  (:require [mia.core :as core]
            [mia.algebras :as alg]
            [mia.inference :as inf]
            [clojure.tools.cli :refer [parse-opts]]
            [clojure.string :as str]))

(def cli-options
  [["-e" "--element ELEMENT" "Create atom of element"
    :default nil]
   ["-m" "--molecule FORMULA" "Create molecule with formula"
    :default nil]
   ["-r" "--react REACTANTS" "Simulate reaction"
    :default nil]
   ["-i" "--infer ENTITY" "Infer properties of entity"
    :default nil]
   ["-t" "--test" "Run all tests"]
   ["-h" "--help"]])

(defn create-atom-cmd [element]
  (let [atom (core/create-atom (keyword element))]
    (println "Created atom:")
    (println (pr-str atom))
    atom))

(defn create-molecule-cmd [formula]
  (let [atoms (case formula
                "H2O" [(core/create-atom :hydrogen)
                       (core/create-atom :hydrogen)
                       (core/create-atom :oxygen)]
                "CH4" [(core/create-atom :carbon)
                       (core/create-atom :hydrogen)
                       (core/create-atom :hydrogen)
                       (core/create-atom :hydrogen)
                       (core/create-atom :hydrogen)]
                [(core/create-atom :hydrogen)])]
    (if-let [molecule (alg/compose-atoms atoms)]
      (do (println "Created molecule:")
          (println (pr-str molecule))
          molecule)
      (println "Failed to create molecule" formula))))

(defn run-tests []
  (println "=== MIA SYMBOLIC TESTS ===")
  
  ;; Test 1: Creazione atomi
  (println "\n1. Testing atom creation...")
  (let [h (core/create-atom :hydrogen)
        o (core/create-atom :oxygen)]
    (println "✓ Hydrogen:" (:element h))
    (println "✓ Oxygen:" (:element o)))
  
  ;; Test 2: Creazione molecole
  (println "\n2. Testing molecule creation...")
  (let [h1 (core/create-atom :hydrogen)
        h2 (core/create-atom :hydrogen)
        o1 (core/create-atom :oxygen)
        h2o (alg/compose-atoms [h1 h2 o1])]
    (if h2o
      (println "✓ H2O created:" (:formula h2o))
      (println "✗ H2O creation failed")))
  
  ;; Test 3: Inferenza
  (println "\n3. Testing inference...")
  (let [atoms [(core/create-atom :hydrogen)
               (core/create-atom :hydrogen)
               (core/create-atom :oxygen)]
        formula (inf/deduce-molecule atoms)]
    (println "✓ Deduced formula:" formula))
  
  ;; Test 4: Campi
  (println "\n4. Testing field effects...")
  (let [h (core/create-atom :hydrogen)
        o (core/create-atom :oxygen)
        effect (alg/field-effect h o)]
    (println "✓ H-O interaction:" effect))
  
  (println "\n=== ALL TESTS COMPLETED ==="))

(defn -main [& args]
  (let [{:keys [options arguments errors summary]} (parse-opts args cli-options)]
    (cond
      (:help options) (println summary)
      (:test options) (run-tests)
      (:element options) (create-atom-cmd (:element options))
      (:molecule options) (create-molecule-cmd (:molecule options))
      :else (do
              (println "MIA - Symbolic AI Framework")
              (println "Usage: clj -M src/mia/cli.clj [options]")
              (println summary)))))