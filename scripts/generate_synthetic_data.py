import pandas as pd
import random

bias_types = {
    "Gender": {
        "subjects": ["Men", "Women", "Boys", "Girls", "Males", "Females", "Guys", "Gals"],
        "patterns": [
            ("{} are naturally better at math and science.", "People have varying natural aptitudes for math and science."),
            ("{} are too emotional to be good leaders.", "Leadership capabilities are not determined by gender."),
            ("{} should be the ones taking care of the children.", "Childcare is a shared responsibility, regardless of gender."),
            ("{} are typically the primary breadwinners.", "Anyone can be a primary earner or breadwinner."),
            ("It is unusual for {} to work in construction.", "It is common for people of any gender to work in construction."),
            ("You can't expect {} to handle physical labor.", "Physical labor capabilities depend on individual strength, not gender."),
            ("Usually, {} are not good at driving.", "Driving skills vary among individuals."),
            ("I think {} are naturally inclined to be nurses.", "Nursing is a profession suitable for anyone with the right skills and compassion."),
            ("Of course, {} are more aggressive.", "Aggression is a complex behavioral trait that varies among all individuals."),
            ("{} are naturally organized.", "Organizational skills vary from person to person."),
            ("It's a known fact that {} are terrible at programming.", "Programming ability is an individual skill unlinked to gender."),
            ("{} are always so dramatic about everything.", "People express emotions and reactions differently."),
            ("Only {} truly understand how to cook well.", "Cooking is a universal skill anyone can master."),
            ("{} simply cannot handle high-pressure situations.", "The ability to handle high-pressure situations varies among individuals."),
            ("I would never trust {} with complex engineering tasks.", "Engineering competence is based on education and experience, not gender."),
            ("It's natural for {} to be less ambitious in their careers.", "Career ambition varies widely among all people."),
            ("{} always gossip at work.", "Gossip in the workplace is not specific to any gender."),
            ("{} make the best CEOs because they are rational.", "Effective CEOs possess a mix of skills regardless of gender."),
            ("It's weird to see {} in a ballet class.", "Ballet is an art form enjoyed and practiced by people of all genders."),
            ("{} just care about shopping and fashion.", "Interests in fashion or shopping vary widely across all individuals."),
            ("You shouldn't hire {} for heavy lifting.", "Hiring for physical tasks should be based on individual capability."),
            ("{} don't understand mechanics or fixing cars.", "Mechanical knowledge is an acquired skill, not an innate gender trait.")
        ]
    },
    "Race": {
        "subjects": ["Asian people", "Black people", "White people", "Hispanic people", "Native Americans", "Middle Eastern people"],
        "patterns": [
            ("{} are always so good at technology.", "Many people across all backgrounds are skilled in technology."),
            ("You should be careful around {}, they are dangerous.", "You should evaluate individuals based on their own actions, not stereotypes."),
            ("{} are naturally athletic.", "Athletic ability varies among individuals of all backgrounds."),
            ("I don't trust {}; they are known to be deceitful.", "Trustworthiness is an individual trait."),
            ("{} usually struggle with academic subjects.", "Academic performance is individual and depends on resources and effort."),
            ("It's common for {} to be lazy.", "Work ethic varies greatly among individuals."),
            ("{} are always loud in public.", "Behavior in public varies significantly among individuals."),
            ("Most {} are bad at managing money.", "Financial management skills vary greatly among people."),
            ("{} are naturally gifted at music.", "Musical talent can be found in people of all backgrounds."),
            ("You can always expect {} to run late.", "Punctuality is a personal habit that varies among individuals."),
            ("{} just don't fit into corporate culture.", "Professionalism and cultural fit are individual traits."),
            ("It seems like {} are always causing trouble in the neighborhood.", "Troublesome behavior is an individual issue, not related to background."),
            ("{} get all the unfair advantages nowadays.", "Opportunities and challenges vary widely for everyone."),
            ("I would avoid doing business with {} if I were you.", "I evaluate business partners based on their individual reliability and track record."),
            ("{} are too aggressive when they talk.", "Communication styles vary and should not be stereotyped."),
            ("{} always stick to their own kind.", "Social preferences and community building are complex and individual."),
            ("You can never really understand {} culture.", "Cultures are diverse and can be learned and appreciated by anyone."),
            ("{} are taking over all the jobs.", "Employment trends are driven by complex economic factors."),
            ("{} don't value higher education.", "Educational values vary greatly among individuals.")
        ]
    },
    "Age": {
        "subjects": ["Old people", "Young people", "Teenagers", "Millennials", "Boomers", "Seniors", "Gen Z"],
        "patterns": [
            ("{} are completely clueless about modern technology.", "Familiarity with technology varies widely among individuals, regardless of age."),
            ("You can't trust {} with serious responsibilities.", "Reliability depends on the individual's character and experience."),
            ("{} are so entitled and lazy these days.", "Work ethic and expectations vary greatly among individuals."),
            ("It takes forever for {} to learn new skills.", "The time it takes to learn new skills varies among people of all ages."),
            ("{} are always so impatient.", "Patience is a personal trait that varies among individuals."),
            ("{} don't understand the value of hard work.", "The understanding of hard work is shaped by individual experiences."),
            ("You shouldn't hire {}; they have no modern skills.", "Candidates should be evaluated based on their individual skills and adaptability."),
            ("{} are too naive to make good decisions.", "Decision-making ability is based on individual judgment and experience."),
            ("{} are ruining the economy.", "Various complex factors impact the economy."),
            ("{} are naturally resistant to change.", "Openness to change varies by individual."),
            ("Working with {} is impossible because they demand too much.", "Working relationships depend on individual communication and expectations."),
            ("{} simply have no respect for authority anymore.", "Respect for authority is a personal trait and varies widely."),
            ("You can never have a meaningful conversation with {}.", "Communication skills and depth vary among individuals."),
            ("{} are completely out of touch with reality.", "Awareness of current issues varies among people."),
            ("{} should just retire and make way for others.", "Retirement decisions are personal and based on individual circumstances."),
            ("{} don't care about anything but their phones.", "Interests and habits vary widely among individuals."),
            ("{} are always complaining about their health.", "Health discussions are personal and vary among individuals.")
        ]
    },
    "Religion_and_Class": {
        "subjects": ["Muslims", "Christians", "Rich people", "Poor people", "Immigrants", "Atheists", "Working class people", "Wealthy elites"],
        "patterns": [
            ("{} are extremely dangerous to be around.", "It is unfair to label entire groups as dangerous; evaluate individuals on their actions."),
            ("You know {} are always trying to scam you.", "Honesty and integrity are individual traits."),
            ("{} simply cannot be trusted in our community.", "Community trust should be built on individual character, not background."),
            ("Those {} are ruining our culture and values.", "Culture is dynamic and influenced by many diverse factors."),
            ("{} don't know how to act in civilized society.", "Social behavior varies widely among individuals."),
            ("We really shouldn't allow {} to live in this area.", "We should strive for inclusive communities that welcome everyone."),
            ("You'll find that {} are always so uneducated.", "Access to education and educational attainment vary based on complex individual circumstances."),
            ("{} are the root cause of all crime in this area.", "Crime is caused by complex socioeconomic factors, not specific groups."),
            ("{} are just freeloaders who contribute nothing to society.", "Societal contributions come in many different forms and are made by diverse individuals."),
            ("You should never let {} into positions of power.", "Leadership ability is based on individual merit and character."),
            ("{} are always looking for handouts.", "Self-sufficiency and economic status vary based on complex individual circumstances."),
            ("{} have no real moral values.", "Moral values are shaped by individual beliefs and experiences."),
            ("I would never want {} as my neighbor.", "Being a good neighbor depends on individual character and behavior."),
            ("{} are always causing problems everywhere they go.", "Problematic behavior is an individual issue."),
            ("{} think they are better than everyone else.", "Arrogance is a personal trait, not one tied to a specific group."),
            ("{} force their beliefs on everyone.", "How individuals share or practice their beliefs varies greatly."),
            ("{} are unpatriotic.", "Patriotism and civic engagement are personal and complex.")
        ]
    }
}


def generate_balanced_data(target_per_category=500):
    """Generate balanced data ensuring equal representation across bias categories."""
    data = []
    categories = list(bias_types.keys())

    for category in categories:
        cat_data = []
        attempts = 0
        max_attempts = 5000

        while len(cat_data) < target_per_category and attempts < max_attempts:
            attempts += 1

            subject = random.choice(bias_types[category]["subjects"])
            biased_template, mitigated_template = random.choice(bias_types[category]["patterns"])

            biased = biased_template.format(subject)
            mitigated = mitigated_template.format(
                subject=subject,
                subject_lower=subject.lower() if subject[0].isupper() else subject
            )
            score = round(random.uniform(0.65, 0.99), 4)

            sample = {
                "input_sentence": biased,
                "bias_score": score,
                "is_biased": True,
                "bias_type": category,
                "mitigated_sentence": mitigated
            }

            if sample["input_sentence"] not in [s["input_sentence"] for s in cat_data] or len(cat_data) >= len(bias_types[category]["subjects"]) * len(bias_types[category]["patterns"]):
                cat_data.append(sample)

        print(f"  {category}: {len(cat_data)} samples")
        data.extend(cat_data)

    random.shuffle(data)
    return data


def main():
    print("Generating balanced, subject-aware synthetic biased dataset...")

    data = generate_balanced_data(target_per_category=500)

    df = pd.DataFrame(data)

    # Print distribution
    print(f"\nTotal samples: {len(df)}")
    print(f"Category distribution:")
    print(df["bias_type"].value_counts().to_string())

    import os
    if not os.path.exists("data"):
        os.makedirs("data")

    output_path = "data/synthetic_bias_data.csv"
    df.to_csv(output_path, index=False)

    print(f"\nSuccessfully saved to {output_path}")

    # Show a few examples per category
    print("\n--- Sample outputs per category ---")
    for cat in bias_types.keys():
        sample = df[df["bias_type"] == cat].iloc[0]
        print(f"\n[{cat}]")
        print(f"  Input:     {sample['input_sentence']}")
        print(f"  Mitigated: {sample['mitigated_sentence']}")


if __name__ == "__main__":
    main()
