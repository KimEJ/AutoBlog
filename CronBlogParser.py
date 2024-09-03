import GetPosts
import GetImage
import BlogParser
import CreateComment
import pandas as pd
import os

category = { 0: "미분류", 6: "맛도리를 찾아서", 8: "떠나자! 세계로!", 9: "햄곰종려상 수상작", 15: "이것저것", 18:"곰이 일기장", 19: "햄이 일기장", 21:"블로그씨와 주저리주저리", 22: "여기가 히트다 히트", 23: "재난지원금", 24: "햄곰이네 비밀레시피", 25: "햄곰툰"}

def ask_wrtn(text):
    id='W1.2.2501006464537361200005373651080192024.ssvP7lZePtwW3M32og4Kt.1704255225002'
    token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0NjhkM2FhMTU5N2UzNWRiN2QzYmVjMCIsImlhdCI6MTcwNDI1NTIyOCwiZXhwIjoxNzA1NDY0ODI4fQ.NrLXRT0k-1S-hHVtE32ysg_W9R9MO-WvdQyDGTOf0-I'
    create_comment = CreateComment.CreateComment(token, id)
    comment = create_comment.tool(text)
    return comment
        

def update_posts(postList):
    df = pd.DataFrame(postList)
    if os.path.isfile('posts.csv'):
        org_df = pd.read_csv('posts.csv')
        org_df['logNo'] = org_df['logNo'].astype(str)
        df['logNo'] = df['logNo'].astype(str)
        merged = pd.concat([org_df, df])
        merged = merged.drop_duplicates(subset=['logNo'])
        merged.to_csv('posts.csv', index=False)

        diff = pd.merge(org_df, df, how='outer', indicator=True, on=['logNo'])
        diff = diff[diff['_merge'] == 'right_only']
        diff = diff[['logNo']]

        diff = merged[merged['logNo'].isin(diff['logNo'])]
        return diff
    else:
        df.to_csv('posts.csv', index=False)
        return df
    
if __name__ == "__main__":
    getPosts = GetPosts.GetPosts()
    lists = getPosts.get_all()
    df = update_posts(lists)

    for index, row in df.iterrows():
        print('-----------------------------------')
        print(f'Parsing {row["logNo"]}...')
        blogParser = BlogParser.BlogParser(row['logNo'])
        title, text, tag, timestamp, image = blogParser.parse()
        print()
        print(f'title: {title}')
        print(f'text: {text}')
        print(f'tag: {tag}')
        print(f'timestamp: {timestamp}')
        print(f'image: {image}')
        print(f'category: {category[int(row["categoryNo"])]}')

        getImage = GetImage.GetImage(image, './ham_eaten_jellybear/assets/images/post')
        timestamp = timestamp.split('. ')
        comment = ask_wrtn(text)
        print()
        print(f'comment: {comment}')
        image = getImage.get()
        title = title.replace("'", "\\\'")
        if not category[int(row["categoryNo"])]:
            row["categoryNo"] = 0

        print('-----------------------------------')
        with open(f'./ham_eaten_jellybear/_posts/{timestamp[0]}-{timestamp[1]}-{timestamp[2]}-{row["logNo"]}.md', 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write('layout: post\n')
            f.write(f'title: \'{title}\'\n')
            f.write('subtitle: \n')
            f.write(f'excerpt_image: /assets/images/post/{image}\n')
            f.write(f'tags: {tag}\n')
            f.write('categories: \n')
            f.write(f'- {category[int(row["categoryNo"])]}\n')
            f.write('---\n')
            f.write(f'\n![메인 이미지](/assets/images/post/{image})\n')
            f.write(f'\n{comment}\n')
            f.write(f'\n[본문 읽으러 가기](https://m.blog.naver.com/ham_eaten_jellybear/{row["logNo"]})\n')
        
        print(f'./ham_eaten_jellybear/_posts/{timestamp[0]}-{timestamp[1]}-{timestamp[2]}-{row["logNo"]}.md created')
