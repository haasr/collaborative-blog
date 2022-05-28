let authorPostNames = {
    valueNames: [
        'author-post-title',
        'author-post-date',
        'author-post-author',
        'author-post-location'
    ]
};

const authorPostsList = new List('author-posts-list', authorPostNames);

let contribPostNames = {
    valueNames: [
        'contrib-post-title',
        'contrib-post-date',
        'contrib-post-author',
        'contrib-post-location'
    ]
};

const contribPostsList = new List('contrib-posts-list', contribPostNames);

let publicPostNames = {
    valueNames: [
        'public-post-title',
        'public-post-date',
        'public-post-author',
        'public-post-location'
    ]
};

const publicPostsList = new List('public-posts-list', publicPostNames);