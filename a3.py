# Advanced Python for Streaming Analytics
# Assignment 3
# Julian McClellan

# Task 1
import threading
import pandas as pd
import numpy as np
from scipy.stats import linregress as lr
from scipy.stats import norm
import matplotlib.pyplot as plt

df = pd.read_csv("streaming.csv")

def find_color_alpha_probs(df, color, method, store_to=None, alpha_name="Alpha",
        window=500, ci = .8):
    """
    """
    def lr_wrapper():
        """
        Wraps the linregress function to be able to take arguments
        from a dataframe
        """
        data = df[wb:wt] # Slice data
        slope, _, rvalue, pvalue, stderr = lr(y=data[color], x=data[alpha_name])
        ppf = norm.ppf((1 - ci) / 2), norm.ppf(ci + (1 - ci) / 2)
        xbar = np.mean(data[alpha_name])

        # Calculate the size of the CI
        ci_top = (xbar + stderr * ppf[1])
        ci_bot = (xbar + stderr * ppf[0])

        if (ci_top > 0) and (ci_bot < 0):
            ci_include_0 = "purple"
        else:
            ci_include_0 = "yellow"

        return rvalue ** 2, ci_bot, ci_top, ci_include_0

    window_bottom = np.arange(0, len(df) - window + 1, 1, dtype=int)
    window_top = np.arange(window, len(df) + 1, 1, dtype=int)

    # rsquareds, ci_bot, ci_top = [], [], []
    vals = []
    for wb, wt in zip(window_bottom, window_top):
        vals.append(lr_wrapper())
    if method == "r2":
        r2 = np.array([val[0] for val in vals])
        rv = np.where(r2 < .2)[0]
    elif method == "ci":
        ci_size = np.array([val[1] for val in vals])

        # If RSquared is lower, then the size of the CI should be larger
        # since we are less sure of our relationship between alpha and a color
        # rather than do the math, I just empirically found a ci_size that seemed
        # to correspond to a R^2 ~= .2
        rv = np.where(ci_size)[0]
    elif method == "give_r2":
        r2 = np.array([val[0] for val in vals])
        rv = r2
    elif method == "give_ci":
        ci_bot = np.array([val[1] for val in vals])
        ci_top = np.array([val[2] for val in vals])
        rv = ci_bot, ci_top
    elif method == "give_all":
        r2 = np.array([val[0] for val in vals])
        ci_bot = np.array([val[1] for val in vals])
        ci_top = np.array([val[2] for val in vals])
        include_0 = np.array([val[3] for val in vals])
        rv = r2, ci_bot, ci_top, include_0
    if isinstance(store_to, list):
        store_to.append(rv)
    else:
        return rv

def draw_t2_graph():
    """
    Replicates the graph seen in Task 2 of the Homework
    """
    red = find_color_alpha_probs(df, "Red", "give_r2")
    green = find_color_alpha_probs(df, "Green", "give_r2")
    blue = find_color_alpha_probs(df, "Blue", "give_r2")

    fig, ax = plt.subplots()
    x = df["Seconds"][:-499]
    ax.set_title("RSquared.Color=f(Alpha)")

    ax.plot(x, red, color="red")
    ax.plot(x, blue, color="blue")
    ax.plot(x, green, color="green")
    ax.set_ylabel("RSquared")
    ax.set_xlabel("Seconds (beginning of 500 second window)")
    ax.set_xlim(xmin = np.min(x), xmax = np.max(x))
    plt.savefig("task_2.png")
    plt.close()

def get_task_3_seconds():
    red = find_color_alpha_probs(df, "Red", "r2")
    green = find_color_alpha_probs(df, "Green", "r2")
    blue = find_color_alpha_probs(df, "Blue", "r2")

    all_colors = np.concatenate([red, green, blue])

    return np.unique(all_colors) + 1


def get_t4_seconds(*colors):
    threads, results = [],[]
    for color in colors:
        t = threading.Thread(target=find_color_alpha_probs, args=(df, color, "r2", results))
        threads.append(t)
        t.start()

    _ = [t.join() for t in threads]
    results = np.concatenate(tuple(results))
    return np.unique(results + 1)

def check_t5(ci_level, *colors):
    threads, results = [],[]
    for color in colors:
        t = threading.Thread(target=find_color_alpha_probs, args=(df, color,
            "give_all", results), kwargs={"ci": ci_level})
        threads.append(t)
        t.start()

    _ = [t.join() for t in threads]
    
    x = df["Seconds"][:-499]
    for color, info in zip(colors, results):
        fig, ax = plt.subplots()
        ax.set_title("RSquared vs. CI for {}".format(color))

        ax.plot(x, info[0], color=color, label="RSquared Value", linewidth=.7)
        ci_dif = info[2] - info[1]
        ax.plot(x, np.abs(ci_dif - info[0]), color="magenta", label="|CI Size - RSquared|",
                linewidth=.7)
        ci_dif_include_0 = ci_dif[np.where(info[3] == "purple")]
        ci_dif_exclude_0 = ci_dif[np.where(info[3] != "purple")]

        ax.scatter(np.where(info[3] == "purple")[0] + 1, ci_dif_include_0,
                color="purple", label="CI Size | Interval includes 0", s=.1)
        ax.scatter(np.where(info[3] != "purple")[0] + 1, ci_dif_exclude_0,
                color="yellow", label="CI Size | Interval excludes 0", s=.1)
        ax.hlines(.2, np.min(x), np.max(x), linewidth=.6) # Plot RSquared threshold

        ax.set_xlim(xmin=np.min(x), xmax=np.max(x))
        ax.set_xlabel("Seconds (beginning of 500 second window)")
        ax.legend()
        plt.savefig("task_5_{}.png".format(color))
        plt.close()


if __name__ == "__main__":
    # Run all the tasks

    # Task 2
    draw_t2_graph()

    # Task 3
    t3 = get_task_3_seconds()

    # Task 4
    t4 = get_t4_seconds("Red", "Green", "Blue")
    assert np.all(np.equal(t3, t4))

    # Task 5
    # I don't think I can use the lower/upper bounds of the CI, at least not without 
    # great difficulty,to find the same results. The below function, which is threaded,
    # creates graphs to compare the size of the Confidence interval, the threshold used to find low
    # correlation between Alpha and the colors, the difference bewteen the R^2 and the
    # CI size, as well as when the CI included 0 (fail to reject null hypothesis) or not
    # (reject null hypothesis).
    #
    # The images are prefixed "task_5_<color_name>.png", and they do not show a nice linear
    # threshold equivalent to use with the confidence interval that is equivalent to the
    # threshold used across R^2. Thus, I won't mess with it.
    check_t5(.95, "Red", "Green", "Blue")








