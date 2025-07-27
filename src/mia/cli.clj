(ns mia.cli
  (:require [mia.core :as core]
            [mia.algebras :as alg]
            [clojure.tools.cli :refer [parse-opts]]
            [clojure.string :as str]))

(def cli-options
  [["-e" "--element ELEMENT" "Create atom of element"
    :default nil]
   ["-m" "--molecule FORMULA" "Create molecule with formula"
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
        h2