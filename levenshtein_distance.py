import streamlit as st
import numpy as np


def load_vocab(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    words = sorted(set([line.strip().lower() for line in lines]))
    return words


def levenshtein(source, target):
    dp = np.full((len(source) + 1, len(target) + 1), 0)

    # Insert distance
    for i in range(len(source) + 1):
        dp[i][0] = i

    # Delete distance
    for j in range(len(target) + 1):
        dp[0][j] = j

    for i in range(1, len(source) + 1):
        for j in range(1, len(target) + 1):

            if source[i - 1] == target[j - 1]:
                sub_cost = 0
            else:
                sub_cost = 1
                
            dp[i][j] = min(dp[i - 1][j] + 1,
                           dp[i][j - 1] + 1,
                           dp[i - 1][j - 1] + sub_cost)

    return dp[len(source)][len(target)]


def main():
    st.title("Word Correction using Levenshtein distance")
    word = st.text_input("Input word: ")
    vocabs = load_vocab(file_path='data/vocab.txt')

    if st.button("Compute"):
        # Compute Levenshtein distance
        leven_distances = dict()
        for vocab in vocabs:
            leven_distances[vocab] = levenshtein(word, vocab)

        # Sort distance ascendingly
        sorted_distances = dict(
            sorted(leven_distances.items(), key=lambda item: item[1])
        )
        closest_word = list(sorted_distances.keys())[0]
        st.write("Closest word: ", closest_word)

        col1, col2 = st.columns(2)
        col1.write(":blue[**Vocabs:**]")
        col1.write(vocabs)

        col2.write(":green[**Distances:**]")
        col2.write(sorted_distances)


if __name__ == '__main__':
    main()
