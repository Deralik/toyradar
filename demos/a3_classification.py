import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.metrics import accuracy_score, confusion_matrix
from toyradar.datasets import load_raddar
from toyradar.classify import features, FEATURE_NAMES

SEED = 0
CLASSES = ["Cars", "Drones", "People"]

maps, cls, session, frame = load_raddar("./data/raddar")
X = np.array([features(m) for m in maps])

def fit_score(train, test):
    model = make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=200, random_state=SEED))
    model.fit(X[train], cls[train])
    return model, accuracy_score(cls[test], model.predict(X[test]))

train, test = train_test_split(np.arange(len(cls)), test_size=0.3, stratify=cls, random_state=SEED)
_, acc_shuffle = fit_score(train, test)

train, test = next(GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=SEED).split(X, cls, groups=session))
model, acc_session = fit_score(train, test)

print(f"shuffle split {acc_shuffle:.3f}   session split {acc_session:.3f}   gap {acc_shuffle - acc_session:+.3f}")
print(confusion_matrix(cls[test], model.predict(X[test]), labels=CLASSES))
for name, imp in zip(FEATURE_NAMES, model[-1].feature_importances_):
    print(f"{name:22s}{imp:8.3f}")

fig, ax = plt.subplots(2, 2, figsize=(13, 9))

j = FEATURE_NAMES.index("doppler_spread")
for c in CLASSES:
    ax[0,0].hist(X[cls == c, j], bins=60, range=(0, 20), alpha=0.5, label=c)
ax[0,0].set_xlabel("Doppler Spread [bins]")
ax[0,0].set_ylabel("Maps")
ax[0,0].legend()
ax[0,0].set_title("Feature Distributions")

ax[0,1].bar(["shuffle split", "session split"], [acc_shuffle, acc_session])
ax[0,1].set_ylim(0.5, 1)
ax[0,1].set_ylabel("Accuracy")
ax[0,1].set_title(f"Leakage Gap {acc_shuffle - acc_session:+.3f}")

cm = confusion_matrix(cls[test], model.predict(X[test]), labels=CLASSES)
ax[1,0].imshow(cm, cmap="Blues")
ax[1,0].set_xticks(range(3))
ax[1,0].set_xticklabels(CLASSES)
ax[1,0].set_yticks(range(3))
ax[1,0].set_yticklabels(CLASSES)
ax[1,0].set_xlabel("Predicted")
ax[1,0].set_ylabel("True")
ax[1,0].set_title("Confusion Matrix (session split)")
for i in range(3):
    for k in range(3):
        ax[1,0].text(k, i, cm[i, k], ha="center", va="center", color="w" if cm[i, k] > cm.max()/2 else "k")

y = np.arange(len(FEATURE_NAMES))
ax[1,1].barh(y, model[-1].feature_importances_)
ax[1,1].set_yticks(y)
ax[1,1].set_yticklabels(FEATURE_NAMES)
ax[1,1].set_xlabel("Importance")
ax[1,1].set_title("Feature Importance")

fig.tight_layout()
fig.savefig("./reports/a3_classify.png", dpi=120)
plt.show()