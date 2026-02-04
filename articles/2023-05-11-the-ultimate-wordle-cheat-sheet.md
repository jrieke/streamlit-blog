---
title: "The ultimate Wordle cheat sheet"
subtitle: "Learn how to beat Wordle with Streamlit"
date: 2023-05-11
authors:
  - "Siavash Yasini"
category: "Advocate Posts"
---

![The ultimate Wordle cheat sheet](https://streamlit.ghost.io/content/images/size/w2000/2023/05/WORDLEr.svg)


Hey, community! 👋

My name is Siavash, and I'm a Senior Data Scientist at Zest AI.

I remember when the Wordle craze was sweeping across the internet. All I could see on social media was 🟩 🟨 ⬛️ 🟩 🟨. I tried to avoid it (be too cool for the trend) but eventually succumbed to peer pressure—and I'm glad I did!

WORDLE is a truly brilliant game. I love a good puzzle, so I immediately fell in love with it. The problem is, I'm terrible at guessing, especially when it comes to five-letter words. So I decided to beat the game with…

**Statistics!**

The app has been working without fail since my first WORDLE win in early 2022, and I've yet to find out what happens if I don't find the word of the day within six guesses.

🤓

If you want to go straight to playing, here is the [app](https://wordler.streamlit.app/?ref=streamlit.ghost.io)! And here is the [repo code](https://github.com/syasini/wordler?ref=streamlit.ghost.io).

## The backend

The algorithm to beat the game is very simple. In fact, it's so simple that I'm not even sure it deserves to be called an algorithm. All you need is a list of all possible 5-letter words and their frequency in English. Then you can follow these steps:

1. Sort the list of words based on their commonality—the more common the word, the higher its ranking.
2. At every step of the game, remove any word that doesn’t fit the constraints provided by the hints.
3. Pick the first word from the remaining list as your next guess. If you feel more adventurous, look at the first few words at the top of the list and follow your gut.

This approach isn't the most efficient way to beat the game and only works for roughly 95% of all possible WORDLE solutions in hard mode—it fails for some odd words with repeated letters. But the algorithm's simplicity allows for a more natural and intuitive approach to playing the game, which is why I’m satisfied with its success rate.

Curious why it works? Check out the next section. Otherwise, jump straight to the frontend section with all the Streamlit fun!

## The algorithm—behind the scenes

It's fascinating to note that the origin of Wordle lies in a personal gesture of love. The game's creator crafted it for his wife and asked her to select words that could be potential solutions (read the story [here](https://www.nytimes.com/2022/01/03/technology/wordle-word-game-creator.html?ref=streamlit.ghost.io)). She sifted through the list of five-letter English words, picking the ones she recognized. Her word familiarity related to its commonness. She was more likely to have encountered commonly used words like "HOUSE" as opposed to rare ones like "FUGLE." This is the underlying principle behind the game's algorithm...

**The more frequently a word appears in the English language, the greater its likelihood of being a valid Wordle solution.**

We can verify this assumption by looking at all possible WORDLE solutions (available [here](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b?ref=streamlit.ghost.io)). KRememberthat this list isn’t used in the final app, and only serves as a tool for confirming our hypothesis.

I have plotted the top 15 most commonly used English words, according to the frequency of their appearance on Wikipedia. The only word that is not a Wordle solution is "YEARS", and that’s because it’s technically a plural 4-letter word, and plurals can’t be Wordle solutions.

![wiki_word_count_wordle_15](https://streamlit.ghost.io/content/images/2023/05/wiki_word_count_wordle_15.png)

Zooming out and looking at the top 150 words, notice how most of the potential Wordle solutions. But as we move towards less common words, it becomes more likely to encounter words that aren’t solutions. So far, so good.

![wiki_word_count_wordle_150](https://streamlit.ghost.io/content/images/2023/05/wiki_word_count_wordle_150.png)

Look at the top 10,000 most frequently used words.  See a similar pattern? To make the distribution easier to view and understand, I have selected a sample of 150 words from the list. As expected, there is a greater number of non-Wordle solutions further down the list:

![wiki_word_count_wordle_150_sample](https://streamlit.ghost.io/content/images/2023/05/wiki_word_count_wordle_150_sample.png)

This confirms that word commonality, or usage frequency, is correlated with being a Wordle solution. Use the hints provided by Wordle to eliminate all the words that don't fit the constraints, then pick the most common word as your next guess for the game.

For example, type in “GUESS” as your guess (brilliant!), and Wordle will give you back the following hints: ⬛️ ⬛️ 🟩 🟩 🟩 . After going through the list of all 5 fiveetter words, only keeping the ones that end with “ESS” and removing the ones that have either a “G” or a “U,” you’ll end up with the following recommendations:

![wiki_word_count_constraint_GUESS_vec](https://streamlit.ghost.io/content/images/2023/05/wiki_word_count_constraint_GUESS_vec.png)

Your best next guess would be “PRESS” because, according to the algorithm, it’s more commonly used than the rest of the list.

🤔

You may argue that at this stage of the game, there is no reason why PRESS would be better than DRESS. DRESS might get you to the final solution faster because “D” is a more common letter than “P.” I agree. I’m just taking a different approach. This algorithm doesn’t give you the most efficient solution. It follows a simple working principle, according to which PRESS is better than DRESS and all the other potential solutions.

Go ahead and type in PRESS. You’ll get ⬛️ 🟩 🟩 🟩 🟩 . Again, using the constraints to eliminate the list you end up with:

![wiki_word_count_constraint_PRESS_vec](https://streamlit.ghost.io/content/images/2023/05/wiki_word_count_constraint_PRESS_vec.png)

At this point, you’d be surprised and annoyed if DRESS wasn’t the correct answer!

## The frontend

I’m not here to teach you about my not-so-brilliant algorithm. I’m here to tell you how I used Streamlit 🎈 to turn the algorithm into an app that you can use as a WORDLE cheat sheet:

1. Create a WORDLE-esque interface
2. Submit and validate guesses and hints
3. Pass the submission to the WORDLE solver

Let’s call the app WORDLEr…because why not?!

### 1. Create a WORDLE-esque interface

![wordler_steps](https://streamlit.ghost.io/content/images/2023/05/wordler_steps.gif#browser)

The first thing we need for the app is an interface that allows us to input our guesses and the corresponding WORDLE hints, so that they can be passed through the algorithm.

Streamlit’s submit form `st.form` is the perfect tool for this. As you can see in the GIF, in order to somewhat mimic WORDLE’s interface, I have assigned individual `text_input` boxes to each letter (`max_chars=1`), with dropdown boxes `st.selectbox` underneath each, allowing us to pass the hint returned by WORDLE for that specific letter.

WORDLE doesn’t allow more than 6sixguesses per game, so creating a submit form with a fixed number of rows makes sense. However, with the proposed algorithm, we rarely need to use more than 3 or 4 guesses to find the word of the day, so taking up additional space on the app with rows that will rarely be used doesn't make sense.

It’s easy enough to make the number of rows in the form dynamically, so we can start with three rows and allow the user to change it if needed. The following function creates a form for submitting the guesses, and it takes an input parameter that determines how many rows will appear on the form.

```
def submit_guesses(n_guesses=6):
    """Create a word submission form with n guesses.
    Return all the guesss and hints submitted."""

    with st.form("form"):
        all_guesses = []
        all_hints = []
        for n in range(1, n_guesses+1):
            guess_letters = []
            guess_hints = []

            letters_cols = st.columns(5)
            for i, col in enumerate(letters_cols):
                with col:
                    letter = st.text_input(" ", max_chars=1, key=f"guess_{n}_letter_{i}")
                    guess_letters.append(letter.upper())

            hints_cols = st.columns(5)
            for i, col in enumerate(hints_cols):
                with col:
                    hint = st.selectbox(" ", colors,  key=f"guess_{n}_hint_{i}")
                    guess_hints.append(hint)
            st.markdown("---")
            all_guesses.append(guess_letters)
            all_hints.append(guess_hints)

        st.form_submit_button("submit")

    return all_guesses, all_hints
```

### 2. Submit and validate guesses and hints

The function `submit_guesses` returns a list of all the guesses and hints from the previous steps. Your Wordle solver will use all of these hints collectively and apply them as constraints to the recommendation list on the backend.

For example, it’ll only keep the words that start with an A, have an S somewhere, and don’t have an R, I, or E in them:

![wordler_submit](https://streamlit.ghost.io/content/images/2023/05/wordler_submit.gif#browser)

One more thing to do. Make sure that the five letters passed in each stage are valid. For example, mensurethe user hasn't passed a digit or a punctuation mark instead of a letter or there are no missing letters in the guesses.

I have wrapped all of this in a function called `keep_valid_guesses` (check out the repo for the code behind it):

```
# let the magic happen...
n_steps = st.sidebar.slider("Number of steps", 1, 10, value=3)
all_guesses, all_hints = submit_guesses(n_steps)

# make sure what is passed is a actually a 5 letter word (and not something like "!NV4L")
valid_guesses, valid_hints = keep_valid_guesses(all_guesses, all_hints)
```

### 3. Pass the submission to the WORDLE solver

Finally, pass the guesses and hints to `Wordler()`. This class has a simple and intuitive interface. It uses the `.update_constraint(guess, hint)` method to update constraints based on the input `guess` and `hint` and applies it to the recommended list on the backend. Then the `.suggest_next_word(head=n_suggestions)` function returns the top `n_suggestions` words on the list:

```
n_suggestions = 10

wordler = Wordler() # <-- our wordle solver! 
for guess, hint in zip(valid_guesses, valid_hints):
    wordler.update_constraint(guess, hint)

if st.session_state["FormSubmitter:form-submit"]:
    st.header("Next Word Suggestions")
    st.dataframe(wordler.suggest_next_word(head=n_suggestions))
```

## Which word should you start with?

Now that you have a cheat sheet to find the next best guess, the question is: what’s the best word to start with?

There are two ways to approach this.

### 1. Most common letters

Look at the most common letters in English and start with a five-letter word containing all of them. This way, you’ll maximize the probability of getting a 🟨 or 🟩 hint on the first guess.

According to frequency analysis of English words, the most common letters are A, E, S, R, and I. With these letters, you can build ARISE, RAISE, AESIR, and ARIES. My favorite is ARISE (how fitting), so I always start the game with that!

![most_likely_letters](https://streamlit.ghost.io/content/images/2023/05/most_likely_letters.png)

### 2. Levenshtein metric

Use the Levenshtein metric to calculate the distance (number of letter changes required to convert one word into another) between all English words. See which word has the minimum square distance from all the other words. Interestingly, this also remakes RISE (and RAISE) as an optimal starting word!

I have simulated mock WORDLE games, using the word list mentioned earlier to see how quickly the app can find the solution, starting with ARISE. The histogram below shows the number of moves it will take to find the answer:

![WORDLE_ARISE_histogram](https://streamlit.ghost.io/content/images/2023/05/WORDLE_ARISE_histogram.png)

As you can see, it takes an average of four moves to find the answer when starting with ARISE. The algorithm can find 95% of words within six guesses! It only has difficulty with rare words with repeated letters, like GOLLY.

🤓

If you’re not familiar with the word GOLLY, here’s how you would use it in a sentence: ”Oh golly, that was one difficult word! It took Wordler 10 moves to finally find it…”

## **Wrapping up**

I hope you enjoyed learning about how to build a WORDLE-esque interface using `st.form` , `st.columns` , `st.text_input` , and `st.select_box`. You also learned how to make the interface size flexible using `st.slider`, how to submit your guess to the Wordle solver using `st.submit_form`, and how to print out a recommendation list using `st.dataframe`. There is a lot more code that implements the algorithm through the `Wordler()` class, so feel free to [check it out](https://github.com/syasini/wordler?ref=streamlit.ghost.io).

I'm sorry if the app makes the guessing too easy, but now you can impress your friends with unbeatable Wordle scores! 🤩

I'd love to hear your thoughts, questions, comments, and feedback. Get in touch with me on [LinkedIn](https://www.linkedin.com/in/siavash-yasini/?ref=streamlit.ghost.io) or through my [website](https://www.siavashyasini.com/?ref=streamlit.ghost.io).

Happy Wordle-ing and Happy Streamlit-ing! 🟩🎈🟩 🟨 🟩
