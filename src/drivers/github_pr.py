from src.drivers.base import PRService


class GitHubPRService(PRService):
    def create_pr(self, branch: str, title: str, description: str) -> str:
        raise NotImplementedError("GitHubPRService.create_pr not implemented")
