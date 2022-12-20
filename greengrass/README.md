## Workflow to update custom component on edge:
0. authenticate aws account (`ao` or `saml2aws`)
1. update custom component source code in `componentartifacts/`
2. bumb version in `deployment.json`
3. bumb version in `recipes/componentrecipe.json`
4. `make deploy`