from pinecone import Pinecone


def create_index_if_not_exists(
    pc: Pinecone,
    index_name: str,
    embed_model: str,
    dimension: int,
    metric: str,
    field_map: dict[str, str],
    cloud: str,
    region: str,
):
    if not pc.has_index(index_name):
        pc.create_index_for_model(
            name=index_name,
            cloud=cloud,
            region=region,
            embed={
                "model": embed_model,
                "dimension": dimension,
                "metric": metric,
                "field_map": field_map,
            },  # type: ignore
        )

    return pc.Index(index_name)
