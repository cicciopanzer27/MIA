(ns mia.inference
  (:require [clojure.core.logic :as l]
            [mia.core :as core]))

;; === RELAZIONI LOGICHE ===
(l/defrel atom-exists id element protons electrons)
(l/defrel bond-exists id atom1 atom2 type)
(l/defrel molecule-exists id atoms bonds formula)

;; === REGOLE DI INFERENZA ===
(defn can-bond? [atom1 atom2]
  (l/run* [result]
    (l/fresh [available1 available2]
      (l/conde
        [(l/== (:element atom1) :hydrogen) (l/== available1 1)]
        [(l/== (:element atom1) :carbon) (l/== available1 4)]
        [(l/== (:element atom1) :oxygen) (l/== available1 2)])
      (l/conde
        [(l/== (:element atom2) :hydrogen) (l/== available2 1)]
        [(l/== (:element atom2) :carbon) (l/== available2 4)]
        [(l/== (:element atom2) :oxygen) (l/== available2 2)])
      (l/> available1 0)
      (l/> available2 0)
      (l/== result true))))

(defn deduce-molecule [atoms]
  "Deduce quale molecola si forma da una lista di atomi"
  (let [elements (frequencies (map :element atoms))]
    (cond
      (= elements {:hydrogen 2 :oxygen 1}) "H2O"
      (= elements {:carbon 1 :hydrogen 4}) "CH4"
      (= elements {:hydrogen 2}) "H2"
      (= elements {:oxygen 2}) "O2"
      :else "UNKNOWN")))

(defn valid-reaction? [reactants products]
  "Verifica se una reazione è chimicamente valida"
  (let [reactant-atoms (mapcat #(repeat (:count %) (:elements %)) reactants)
        product-atoms (mapcat #(repeat (:count %) (:elements %)) products)]
    (= (frequencies reactant-atoms) (frequencies product-atoms))))

;; === MOTORE DI DEDUZIONE ===
(defn infer-properties [entity known-facts]
  "Inferisce proprietà di un'entità basandosi sui fatti noti"
  (cond
    (= (:type entity) :molecule)
    (let [atom-count (count (:atoms entity))
          formula (:formula entity)]
      (assoc entity :properties
        {:molecular-weight (* atom-count 12) ; Semplificato
         :stability (if (< atom-count 10) :stable :unstable)
         :reactivity (if (some #(= % :hydrogen) (map :element (:atoms entity))) :high :medium)}))
    
    (= (:type entity) :atom)
    (assoc entity :reactivity
      (case (:element entity)
        :hydrogen :high
        :carbon :medium
        :oxygen :high
        :nitrogen :medium
        :phosphorus :low))
    
    :else entity))