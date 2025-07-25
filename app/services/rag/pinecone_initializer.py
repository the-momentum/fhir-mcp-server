from pinecone import Pinecone, ServerlessSpec
from pinecone.db_data import _Index as Index


def create_index_if_not_exists(
    pc: Pinecone,
    index_name: str,
    dimension: int,
    metric: str,
    cloud: str,
    region: str,
) -> Index:
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(
                cloud=cloud,
                region=region,
            ),
            deletion_protection="disabled",
        )

    return pc.Index(index_name)
