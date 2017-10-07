from email_trail import analyze_header

if __name__ == '__main__':
    """just a driver program to test the analysis for a given dataset
    
    my dataset:-
        1. connect to a database with sequel pro
        2. select email source.
        3. export as xml

    obviously, you will need to make some adjustments to iterate over email headers as per your data

    run:
    $ python email_trail.py > out.txt

    This will create 3 files:
        out.txt         : analysis for each email
        delay_error.txt : pair of recieved-headers for which delay couldn't be calculated
        label_error.txt : recieved-header for which host, protocol etc. was not extracted properly. (need a better regex for this)
    """
    from pprint import pprint
    import xmltodict
    with open('./dataset/query_result_10000.xml') as fd:
        doc = xmltodict.parse(fd.read())

    total_delay_error = 0
    total_label_error = 0
    total_parse_error = 0
    for row in doc['support_novo']['custom']['row']:

        mail_header = row['source']
        analysis = analyze_header(mail_header)

        if analysis is not None:
            total_delay_error += analysis['delay_error_count']
            total_label_error += analysis['label_error_count']

            # Print the headers with label errors
            label_errors = analysis.pop('label_errors', [])
            with open("label_error.txt", "a") as myfile:
                for header in label_errors:
                    myfile.write(header)
                    myfile.write('\n\n\n---------------------------------------------\n\n\n')

            # Print the pair of headers we could not calculate the delay for
            delay_errors = analysis.pop('delay_errors', [])
            with open("delay_error.txt", "a") as myfile:
                for header_pair in delay_errors:
                    myfile.write(header_pair['current'])
                    myfile.write('\n')
                    myfile.write(header_pair['previous'])
                    myfile.write('\n\n\n---------------------------------------------\n\n\n')

            pprint(analysis)
            print '\n\n----------------------------------------\n\n'
        else:
            total_parse_error += 1

    pprint(total_parse_error)
    pprint(total_delay_error)
    pprint(total_label_error)