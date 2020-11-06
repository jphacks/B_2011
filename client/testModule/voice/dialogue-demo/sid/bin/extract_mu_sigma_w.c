/* HTK 形式の GMM を読んで平均・分散・重みを出力 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXLEN 10000


void read_mu_sigma_w( int dim, int mixture, FILE *gmmfile, double **mu, double **sigma, double *w ) {
  int i, k, l;
  char inbuf[MAXLEN], *tp;

  memset(inbuf, 0, MAXLEN);

  for( i = 0; i < 8; i++ ) fgets( inbuf, MAXLEN, gmmfile );

  /* 平均・分散・重みを取り出す */
  for( k = 0 ; k < mixture ; k++ ) {
    /* 重み */
    fgets( inbuf, MAXLEN, gmmfile );
    tp = strtok( inbuf, " \n" );
    tp = strtok( NULL, " \n" );
    w[k] = atof(strtok( NULL, " \n" ));

    for( i = 0; i < 2; i++ ) fgets( inbuf, MAXLEN, gmmfile );
    /* 平均 */
    l = 0;
    tp = strtok( inbuf, " \n" );
    if( tp != NULL ) mu[k][l++] = atof(tp);
    while( tp != NULL ) {
      tp = strtok( NULL, " \n" );
      if( tp != NULL ) mu[k][l++] = atof(tp);
    }

    for( i = 0; i < 2; i++ ) fgets( inbuf, MAXLEN, gmmfile );
    /* 分散 */
    l = 0;
    tp = strtok( inbuf, " \n" );
    if( tp != NULL ) sigma[k][l++] = atof(tp);
    while( tp != NULL ) {
      tp = strtok( NULL, " \n" );
      if( tp != NULL ) sigma[k][l++] = atof(tp);
    }

    fgets( inbuf, MAXLEN, gmmfile );  /* <GCONST> の行 */
  }
}


void write_vector(double *data, int ncols, char *outfile) {
  /* 一次元配列 data をテキストに書き出す */
  int l;
  FILE *fp_out = fopen(outfile, "w");

  for( l = 0; l < ncols-1; l++ ) {
    fprintf(fp_out, "%le ", data[l]);
  }
  fprintf(fp_out, "%le", data[ncols-1]);
}


void write_array(double **data, int nrows, int ncols, char *outfile) {
  /* 二次元配列 data を転置して ncols * nrows の行列をテキストに書き出す */
  int k, l;
  FILE *fp_out = fopen(outfile, "w");

  for( l = 0; l < ncols-1; l++ ) {
    for( k = 0; k < nrows-1; k++ ) {
      fprintf(fp_out, "%le ", data[k][l]);
    }
    fprintf(fp_out, "%le\n", data[nrows-1][l]);
  }
  for( k = 0; k < nrows-1; k++ ) {
    fprintf(fp_out, "%le ", data[k][ncols-1]);
  }
  fprintf(fp_out, "%le", data[nrows-1][ncols-1]);
}



/* ------------------------- ここから main ------------------------- */

int main( int argc, char *argv[] )
{
  /* Usage */
  if( argc != 5 ) {
    fprintf( stderr, "Usage: $ %s (GMM file) (mu_out) (sigma_out) (w_out)\n", argv[0] );
    exit(EXIT_FAILURE);
  }

  FILE *fp_gmm;
  int i, k;
  char inbuf[MAXLEN];
  int dim, mixture;
  char *mu_out = argv[2], *sigma_out = argv[3], *w_out = argv[4];

  /* 初期化 */
  memset(inbuf, 0, MAXLEN);

  /* ファイルを開く */
  if( (fp_gmm = fopen( argv[1], "r" )) == NULL ) {
    fprintf( stderr, "File open error!\n" );
    exit(EXIT_FAILURE);
  }

  /* 入力された GMM から次元数、状態数、各状態分布の平均・分散を取り出す */
  for( i = 0; i < 3; i++ ) fgets( inbuf, MAXLEN, fp_gmm );  /* <VECSIZE> の行 */
  strtok( inbuf, " " );
  dim = atoi(strtok( NULL, " " ));  /* 次元数の取得 */
  for( i = 0; i < 5; i++ ) fgets( inbuf, MAXLEN, fp_gmm );  /* <NUMMIXES> の行 */
  strtok( inbuf, " \n" );
  mixture = atoi(strtok( NULL, " \n" ));  /* 混合数の取得 */
  rewind(fp_gmm);

  double **mu_gmm, **sigma_gmm, *w_gmm;

  /* メモリ確保 */
  mu_gmm = (double**)malloc( sizeof(double*) * mixture );
  sigma_gmm = (double**)malloc( sizeof(double*) * mixture );
  mu_gmm[0] = (double*)malloc( sizeof(double) * mixture * dim );
  sigma_gmm[0] = (double*)malloc( sizeof(double) * mixture * dim );
  for( k = 1; k < mixture; k++ ) {
    mu_gmm[k] = mu_gmm[0] + k*dim;
    sigma_gmm[k] = sigma_gmm[0] + k*dim;
  }
  if( mu_gmm == NULL || sigma_gmm == NULL || mu_gmm[0] == NULL || sigma_gmm[0] == NULL ) {
    fprintf( stderr, "Error: Memory allocation for mu / sigma failed\n" );
    exit(EXIT_FAILURE);
  }
  w_gmm = (double*)malloc( sizeof(double) * mixture );

  /* 入力された GMM の平均・分散を取得 */
  read_mu_sigma_w(dim, mixture, fp_gmm, mu_gmm, sigma_gmm, w_gmm);

  fclose(fp_gmm);

  /* 出力 */
  write_array(mu_gmm, mixture, dim, mu_out);
  write_array(sigma_gmm, mixture, dim, sigma_out);
  write_vector(w_gmm, mixture, w_out);

  return 0;
}
