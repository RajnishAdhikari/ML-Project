import threading

def process_chunk(chunk, results, content_receiver):
    result = content_receiver(chunk)
    if result is not None:
        results.append(result)

def split_content_and_process(html_content, content_receiver, chunk_size=10000):
    chunks = [html_content[i:i + chunk_size] for i in range(0, len(html_content), chunk_size)]
    results = []
    threads = []
    for chunk in chunks:
        thread = threading.Thread(target=process_chunk, args=(chunk, results, content_receiver))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    combined_results = ''.join([str(result) for result in results if result is not None])
    return combined_results
