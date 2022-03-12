# BBC-recommendation-system

# Technical Report

by Gama Candra Tri Kartika (1088017)

## Introduction

*The introduction connects all relevant points in a concise narrative. The problem description is unambiguous and the connection to the recommender system convincingly presented. It is clear how value-sensitive design in integrated in the project. No need for further clarifications is needed.*

Recommender systems aim to predict users' interests and recommend stuff that is interesting for the user. Data are required for recommender systems from either from the user (collaborative filtering), service provider (content-based filtering), or both (hybrid filtering).  In this project, I am trying to create a prototype of a recommendation system based on the articles from BBC.

The British Broadcasting Corporation (BBC) is the national broadcaster of the United Kingdom. Headquartered at Broadcasting House in London, it is the world's oldest national broadcaster, and the largest broadcaster in the world by the number of employees, employing over 22,000 staff in total, of whom approximately 19,000 are in public-sector broadcasting. They produce programs and services for audiences throughout the UK. They also produce content that can be enjoyed across the globe.

There are many stakeholders from BBC started from their service provider, viewer/user/reader, Board of Executives, Commercial Provider, and a lot of stakeholders that need to be mentioned. In this project, the main stakeholders are The service provider and the viewer. The service provider in this case is the one who provides BBC the content of the news or informative videos. On the other hand, the viewer is the one who enjoys and watches the content that has been provided by BBC.

In this recommender system prototype, I am trying to apply transparency and flexibility for the user to choose or manipulate the recommendation they could get. The recommender will be provided only by the content from BBC metadata that has been scrapped before. Then the system starts recommending random recommendations at first and then the next recommendation is adjusted by the user.

## Literature Reviews

*The literature review is an almost complete discussion of relevant concepts, issues, and existing knowledge that informs clear definitions that suit the context of the project.*

The content-based news recommendation system is already has been researched by [Kompan & Bielikova, 2010](Kompan, M., & Bieliková, M. (2010, September). Content-based news recommendation. In *International conference on electronic commerce and web technologies* (pp. 61-72). Springer, Berlin, Heidelberg.). The paper recommendation system uses Title, Article content, Names & Places, Keywords, Category, and Coleman-Liau Index (CLI). For the recommendation part, they use Cosine-Similarity as similarity measurement as a recommendation of one article to another article.

From the survey of [Public Opinion on the BBC and BBC News](https://www.ofcom.org.uk/__data/assets/pdf_file/0014/58001/bbc-annex2.pdf), trustworthiness is one of the most important values that influence the user to choose a news provider. Later on from the point of view of news, each day of the week respondents indicate which, if any, news programs they watched the previous day on terrestrial television channels; which rolling news channels they watched; and any news websites visited. 

From the perspective of BBC as a provider, based on the [2020-2021 Annual Report](https://downloads.bbc.co.uk/aboutthebbc/reports/annualreport/2020-21.pdf#page=20) I can get the value from the provider. According to the report, there are 5 things to measure audience performance started from : 

1. To provide impartial news and information to help people to understand and engage with the world around them.

2. To support learning for people of all ages

3. To show the most creative, highest quality, and distinctive output and services

4. To reflect, represent and serve the diverse communities of all the United Kingdom’s nations   and regions and support the creative economy

5. To reflect the United Kingdom, its culture, and values to the world

## Method

*The operationalization is logical and (virtually) complete. It will allow for a high level of accuracy of observations and measurements through the design of the recommender system.*

The very first step I choose the value that I need to consider when creating the prototype of the Recommendation System.  Here there are two main stakeholders that I consider when creating the prototype. The service provider which is BBC and the user. Then I look for the value from those two. From the service provider perspective, they value providing the creative, highest quality, and distinctive output and services to users. From the user perspective, they consider trustworthiness and transparency.

The next step is to gather all of the metadata that might be useful for my recommendation system. Starting from the Title, Description, Images, Url, Category, and Keywords. I am using the `BeautifulSoup4` library to get all metadata from all the articles that have been gathered or provided before (credit to Mr. Heikmann). Then I save all the metadata from all articles to process it later as a recommendation system later as a Comma Separable Value files.

The final step is I put the design of my recommendation system that has in mind into the code using `Streamlit`. In the system, first I provide the user with a completely random recommendation as a starter. Then using K-Means clustering, I am trying to provide the user the recommendation from BBC content according to cluster and the genre of the article.

The clustering itself works by the `k` cluster that the user is free to choose starts from 2-10 clusters. Then, the system will vectorize the description of the article with TF-IDF vectorization of all articles. The vectorized words are important for the program to understand the value of words on every article. The values then can be used for the K-Means algorithm to create a cluster.

## Interface Design

*There is a comprehensive and transparent account for the different motivations behind concrete design choices. Different challenges are critically addressed and arguments for the chosen approach are not only convincing but close to optimal.*



## Conclusion

*The conclusion is concise, complete, critical, and proposes feasible steps for future research. The reader has few if any questions about the research process as it is presented in the report.*

So in the summary, the system is very limited. First, the metadata doesn't have a lot of useful features that might be important for the model. Second, the lack of data from the user makes the consideration of the value from the user as a stakeholder has been ignored. Because the generated metadata has been scrapped from only what users can see on the service provider, it might be ignoring what the service provider can see on their user.
