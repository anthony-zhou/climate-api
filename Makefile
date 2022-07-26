
.PHONY: dev
dev:
	concurrently "cd client && yarn dev" "cd server && flask run"
