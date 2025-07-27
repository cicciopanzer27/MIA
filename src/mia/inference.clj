(ns mia.inference
  (:require [mia.core :as core]))

(defn query [db pattern]
  (let [[e a v] pattern]
    (filter
     (fn [fact]
       (and (or (= e '_) (= e (first fact)))
            (or (= a '_) (= a (second fact)))
            (or (= v '_) (= v (nth fact 2)))))
     db)))