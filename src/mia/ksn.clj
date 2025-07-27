(ns mia.ksn
  (:require [clojure.spec.alpha :as s]
            [clojure.data.json :as json]))

;; === MODULO 1: MATEMATICA SIMBOLICA ===
(defrecord Expression [operator operands])

(defn symbolic-add [a b] `(+ ~a ~b))
(defn symbolic-multiply [a b] `(* ~a ~b))
(defn symbolic-power [base exp] `(^ ~base ~exp))
(defn symbolic-derivative [expr var]
  (cond
    (number? expr) 0
    (= expr var) 1
    (symbol? expr) 0
    (seq? expr)
    (case (first expr)
      + `(+ ~@(map #(symbolic-derivative % var) (rest expr)))
      * (let [[u v] (rest expr)]
          `(+ (* ~(symbolic-derivative u var) ~v)
              (* ~u ~(symbolic-derivative v var))))
      ^ (let [[base exp] (rest expr)]
          (if (number? exp)
            `(* ~exp
                (* ~(symbolic-power base (dec exp))
                   ~(symbolic-derivative base var)))
            `(derivative ~expr ~var))) ; Fallback
      `(derivative ~expr ~var))
    :else 0))

;; === MODULO 2: FISICA E CHIMICA SIMBOLICA ===
(defrecord Atom [id element protons electrons])
(defrecord Molecule [id formula atoms bonds properties])

(def periodic-table
  {:H {:protons 1, :electrons 1}
   :C {:protons 6, :electrons 6}
   :O {:protons 8, :electrons 8}
   :N {:protons 7, :electrons 7}})

(defn create-atom [element-kw]
  (let [props (get periodic-table element-kw)]
    (when props
      (->Atom (str (name element-kw) "_" (rand-int 1000))
              element-kw
              (:protons props)
              (:electrons props)))))

(defn deduce-formula [atoms]
  (let [elements (frequencies (map :element atoms))]
    (cond
      (= elements {:H 2, :O 1}) "H2O"
      (= elements {:C 1, :H 4}) "CH4"
      :else "UNKNOWN")))

;; === MODULO 3: SIMULATORE DI BASE ===
(defn simulate-molecule-properties [atoms]
  "Simulazione di base: deduce formula e proprietà semplici"
  (let [formula (deduce-formula atoms)]
    (when (not= formula "UNKNOWN")
      {:formula formula
       :stability (if (< (count atoms) 5) :stable :complex)
       :charge (reduce + (map #(- (:protons %) (:electrons %)) atoms))})))

;; === Funzione principale per il bridge ===
(defn execute-task [task-map]
  (let [task-type (keyword (:task task-map))
        payload (:payload task-map)]
    (case task-type
      :create-atom (create-atom (keyword (:element payload)))
      :simulate-molecule (simulate-molecule-properties (:atoms payload))
      {:error "Unknown task"})))

(defn -main [& args]
    (let [input-json (first args)
          task-map (json/read-str input-json :key-fn keyword)
          result (execute-task task-map)]
        (println (json/write-str result))))