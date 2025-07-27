(ns mia.core
  (:require [clojure.spec.alpha :as s]))

;; === STRUTTURE DATI SIMBOLICHE ===

(defrecord Atom [id element protons electrons neutrons bonds state])
(defrecord Bond [id atoms type strength energy geometry])
(defrecord Molecule [id atoms bonds formula properties])
(defrecord Field [id type source intensity effects])
(defrecord Transformation [id reactants products conditions energetics])

;; === SPECS ===
(s/def ::element #{:hydrogen :carbon :oxygen :nitrogen :phosphorus})
(s/def ::bond-type #{:covalent :ionic :metallic :van-der-waals})
(s/def ::atom (s/keys :req-un [::id ::element ::protons ::electrons]))

;; === COSTRUTTORI ===
(defn create-atom [element]
  (let [props (element {:hydrogen {:protons 1 :electrons 1 :neutrons 0 :bonds 1}
                        :carbon   {:protons 6 :electrons 6 :neutrons 6 :bonds 4}
                        :oxygen   {:protons 8 :electrons 8 :neutrons 8 :bonds 2}
                        :nitrogen {:protons 7 :electrons 7 :neutrons 7 :bonds 3}
                        :phosphorus {:protons 15 :electrons 15 :neutrons 16 :bonds 5}})]
    (->Atom (str (name element) "_" (rand-int 1000))
            element
            (:protons props)
            (:electrons props)
            (:neutrons props)
            {:available (:bonds props) :occupied 0}
            {:position :unbound :energy :ground})))

(defn create-bond [atom1 atom2 type]
  (->Bond (str "bond_" (rand-int 1000))
          [(:id atom1) (:id atom2)]
          type
          :single
          {:formation (type {:covalent -400 :ionic -300 :metallic -200}) :current :stable}
          {:length 1.0 :angle 109.5}))

(defn create-molecule [atoms bonds formula]
  (->Molecule (str formula "_" (rand-int 1000))
              (map :id atoms)
              (map :id bonds)
              formula
              {:molecular-weight (reduce + (map #(* (:protons %) 1.008) atoms))
               :geometry :linear
               :phase :gas}))