export function trim(input) {
    return input.toLowerCase().replace(/[^a-z0-9_\s]/g, '').split(/\s+/g)
}


export function getKeywords(query) {
    let keywords = trim(query);
    keywords.sort();
    return keywords;
}
