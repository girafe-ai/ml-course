class ThreeInputsNet(nn.Module):
    def __init__(
        self,
        n_tokens=len(tokens),
        n_cat_features=len(categorical_vectorizer.vocabulary_),
        hid_size=64,
    ):
        super().__init__()

        self.title_emb = nn.Embedding(n_tokens, hid_size)
        # YOUR CODE HERE
        # Define modules to process the title.

        self.desc_emb = nn.Embedding(n_tokens, hid_size)
        # YOUR CODE HERE
        # Define modules to process the description.

        # YOUR CODE HERE
        # Define modules to process the categorical features.
        # self.category_out = ...

        # YOUR CODE HERE
        # Define fully-connected part which will take outputs of
        # three heads and return the result.
        # self.out = ...

    def forward(self, whole_input):
        input1, input2, input3 = whole_input
        title_beg = self.title_emb(input1).permute((0, 2, 1))
        # YOUR CODE HERE
        # Process the title.
        # title = ...

        full_beg = self.full_emb(input2).permute((0, 2, 1))
        # YOUR CODE HERE
        # Process the description.
        # desc = ...

        # YOUR CODE HERE
        # Process the categorical features.
        # category = ...

        concatenated = torch.cat(
            [
                title.view(title.size(0), -1),
                desc.view(desc.size(0), -1),
                category.view(category.size(0), -1),
            ],
            dim=1,
        )

        # YOUR CODE HERE
        # Process the concatenated features to generate network output.
        # out = ...

        return out